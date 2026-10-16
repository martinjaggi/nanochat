"""Disposable kernel warmup followed by exact model/optimizer/data/RNG reset."""
import copy,gc,time,torch


def warmup_training(model,original,optimizer,recorder,loader,x,y,cursor,build_loader,accumulation,updates):
    assert updates>0
    torch.cuda.synchronize();start=time.perf_counter()
    state={n:t.detach().clone() for n,t in original.state_dict().items()}
    opt_state=copy.deepcopy(optimizer.state_dict())
    cpu_rng=torch.get_rng_state();gpu_rng=torch.cuda.get_rng_state()
    first_x=x.clone();first_y=y.clone();recorder.warming_up=True
    for _ in range(updates):
        for _ in range(accumulation):
            if hasattr(optimizer,'set_batch'):optimizer.set_batch(x,y)
            loss=model(x,y)
            if hasattr(optimizer,'set_loss'):optimizer.set_loss(loss)
            (loss/accumulation).backward()
            x,y,cursor=next(loader)
        for group in optimizer.param_groups:
            group['lr']=group['initial_lr']*.1
            if group['kind']=='muon':group['momentum']=.85
        optimizer.step();model.zero_grad(set_to_none=True)
    extra=getattr(optimizer,'extra_forward_evals',0)
    original.load_state_dict(state);optimizer.load_state_dict(opt_state);model.zero_grad(set_to_none=True)
    assert all(torch.equal(t,state[n]) for n,t in original.state_dict().items()),'warmup model reset failed'
    torch.set_rng_state(cpu_rng);torch.cuda.set_rng_state(gpu_rng)
    loader=build_loader();x,y,cursor=next(loader)
    assert torch.equal(x,first_x) and torch.equal(y,first_y),'warmup data prefix reset failed'
    # This tokenizer/loader has no random sampling. Preserve intended model RNG.
    torch.set_rng_state(cpu_rng);torch.cuda.set_rng_state(gpu_rng)
    del state,opt_state,first_x,first_y
    gc.collect();gc.freeze();gc.disable()
    torch.cuda.synchronize();seconds=time.perf_counter()-start
    recorder.warming_up=False;recorder.warmup_updates=updates;recorder.warmup_seconds=seconds
    recorder.warmup_extra_forwards=extra;recorder.emit('disposable_warmup',updates=updates,
        fresh_gradient_evals=updates,microbatch_gradient_passes=updates*accumulation,
        extra_batch_forwards=extra,seconds=seconds,model_optimizer_data_rng_reset=True)
    return loader,x,y,cursor
