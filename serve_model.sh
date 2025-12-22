
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export MPLBACKEND=Agg
export PYTHONWARNINGS="ignore:findfont"
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"

vllm serve /mnt/nlpai-storage/eval_team/hf_ckpt/SFT/ckpt/stg3-1120-SFT-train_multiturn_251127_gbs-512_lr-1e-5_minlr-4e-6/iter_0002190/hf \
    --dtype auto \
    --served-model-name VAETKI \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --trust_remote_code \
    --tensor-parallel-size 8 
    # --gpu-memory-utilization 0.9
