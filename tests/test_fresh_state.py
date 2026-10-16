import torch
from research.unnormalized_muon.fresh_state import named_momenta


def test_named_stacked_momentum_partition():
    model=torch.nn.Module();model.register_parameter('wide',torch.nn.Parameter(torch.zeros(2,3)));model.register_parameter('other',torch.nn.Parameter(torch.zeros(2,3)))
    opt=torch.optim.SGD([dict(params=list(model.parameters()),kind='muon')],lr=.01)
    opt.state[model.wide]['momentum_buffer']=torch.arange(12.).reshape(2,2,3)
    result=named_momenta(model,opt)
    assert torch.equal(result['wide'],torch.arange(6.).reshape(2,3))
    assert torch.equal(result['other'],torch.arange(6.,12.).reshape(2,3))
    result['wide'].zero_();assert opt.state[model.wide]['momentum_buffer'][0].count_nonzero()==5


def test_reserved_training_file_does_not_read_main_or_validation(monkeypatch):
    import nanochat.dataloader as d
    read=[]
    class Column:
        def to_pylist(self):return ['document']*128
    class Row:
        def column(self,name):return Column()
    class File:
        num_row_groups=1
        def __init__(self,path):read.append(path)
        def read_row_group(self,i):return Row()
    class Tokenizer:
        def get_bos_token_id(self):return 1
        def encode(self,docs,**kwargs):return [[1,2,3,4,5] for _ in docs]
    monkeypatch.setattr(d.pq,'ParquetFile',File)
    it=d.tokenizing_distributed_data_loader_with_state_bos_bestfit(Tokenizer(),2,4,'train',device='cpu',buffer_size=2,parquet_paths=['reserved-fit','validation'])
    x,y,c=next(it)
    assert read==['reserved-fit'] and x.shape==(2,4) and torch.equal(y[0],torch.tensor([2,3,4,5]))
