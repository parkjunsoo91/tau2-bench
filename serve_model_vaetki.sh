# 1. Configure
export VLLM_WORKER_MULTIPROC_METHOD=spawn
export MPLBACKEND=Agg
export PYTHONWARNINGS="ignore:findfont"
export CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7"
export CHECKPOINT_PATH="/mnt/ckpt/jaycha/sft_checkpoints/v32/iter_0001600/hf"
export NUM_TENSOR_PARALLEL=8

# 2. Serve the model
vllm serve $CHECKPOINT_PATH \
    --dtype auto \
    --served-model-name VAETKI \
    --enable-auto-tool-choice \
    --tool-call-parser hermes \
    --trust_remote_code \
    --tensor-parallel-size $NUM_TENSOR_PARALLEL 
