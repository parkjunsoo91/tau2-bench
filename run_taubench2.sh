# git clone https://github.com/sierra-research/tau2-bench.git
# cp .env tau2-bench/.env
# cd tau2-bench
# uv venv --yes
# source .venv/bin/activate --yes
# uv pip install -e .

export HOSTED_VLLM_API_BASE="http://localhost:8000/v1"

# 1. Configure
NUM_TASKS=3
NUM_TRIAL=1
USER_LLM_NAME="gpt-4o-mini"

# 2. Run the TauBench2
uv run tau2 run --domain airline \
    --agent-llm hosted_vllm/VAETKI \
    --user-llm $USER_LLM_NAME \
    --num-trials $NUM_TRIAL \
    --num-tasks $NUM_TASKS \
    --log-level DEBUG