#!/usr/bin/env bash
set -euo pipefail
out="$1"
export NANOCHAT_DTYPE=bfloat16 NANOCHAT_ATTENTION=fa4
export OMP_NUM_THREADS=8 RAYON_NUM_THREADS=8
export TRITON_PTXAS_PATH=/mloscratch/homes/mljaggi/nanochat-b300/.venv-b300/lib/python3.12/site-packages/nvidia/cuda_nvcc/bin/ptxas
export TORCHINDUCTOR_CACHE_DIR=/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/shared/inductor
export TRITON_CACHE_DIR=/mloscratch/homes/mljaggi/nanochat-unnormalized-muon-runs/shared/triton
py=/mloscratch/homes/mljaggi/nanochat-b300/.venv-b300/bin/python
cd "$out/source"
exec > "$out/run.log" 2>&1
export UNNORMALIZED_BASE_OPTIM="$out/base/nanochat/optim.py"
"$py" -c 'import torch; assert torch.cuda.device_count()==1 and "B300" in torch.cuda.get_device_name(0); print(torch.cuda.get_device_name(0),flush=True)'
if [[ "$(basename "$out")" == *smoke* ]]; then
 "$py" -m pytest tests/test_unnormalized_muon_gpu.py -q -s
 "$py" -m research.unnormalized_muon.run --output "$out/native" --config research/unnormalized_muon/configs/smoke-native.json
 "$py" -m research.unnormalized_muon.run --output "$out/scaled" --config research/unnormalized_muon/configs/smoke-scaled.json
else
 if "$py" -c 'import json,sys; raise SystemExit(0 if json.load(open(sys.argv[1])).get("gpu_checks") else 1)' "$out/config.json"; then
  "$py" -m pytest tests/test_unnormalized_muon_gpu.py -q -s
 fi
 if "$py" -c 'import json,sys; raise SystemExit(0 if json.load(open(sys.argv[1])).get("fresh_diagnosis") else 1)' "$out/config.json"; then
  "$py" -m research.unnormalized_muon.fresh_probe --output "$out" --config "$out/config.json"
 else
  "$py" -m research.unnormalized_muon.run --output "$out" --config "$out/config.json"
 fi
fi
