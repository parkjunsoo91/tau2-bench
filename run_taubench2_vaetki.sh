export HOSTED_VLLM_API_BASE="http://localhost:8000/v1"

# 1. Configure
NUM_TRIAL=1
AGENT_LLM_NAME=hosted_vllm/VAETKI
USER_LLM_NAME="gpt-4.1-2025-04-14"
DOMAIN="telecom"

# 2. Run the TauBench2
tau2 run --domain $DOMAIN \
    --task-split base \
    --max-concurrency 16 \
    --agent-llm $AGENT_LLM_NAME \
    --user-llm $USER_LLM_NAME \
    --num-trials $NUM_TRIAL
