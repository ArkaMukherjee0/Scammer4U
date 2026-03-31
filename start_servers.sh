#!/bin/bash
# ============================================================================
# Start All Benchmark Environment Servers
# ============================================================================
# Launches all 10 benchmark environment servers as background processes.
#
# Usage:
#   bash start_servers.sh          # Start all servers
#   bash start_servers.sh stop     # Stop all servers
#   bash start_servers.sh status   # Check which are running
# ============================================================================

ROOT="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$ROOT/.server_pids"

# ── Server definitions ────────────────────────────────────────────────
NAMES=(
    "cluttered_downloads"
    "coc_gems"
    "github_phish"
    "job_portal"
    "gov_portal"
    "ecommerce"
    "news"
    "marketplace"
    "summarizer"
    "freelance"
)

CMDS=(
    "uv run python cluttered-downloads/app.py"
    "uv run python coc-gems/app.py"
    "uv run python subfolder/app.py"
    "uv run python job-app-website/run_servers.py"
    "uv run python gov-portal-site/run_servers.py"
    "uv run python ecommerce-platform/run_servers.py"
    "uv run python news-content-site/run_servers.py"
    "uv run python marketplace-website/app.py"
    "uv run python summary-website/app.py"
    "uv run python freelance-platform/run_servers.py"
)

PORTS=(
    "5050"
    "5051"
    "5053"
    "8025"
    "8050"
    "10010"
    "8040"
    "5052"
    "5054"
    "9010"
)

# ── Stop all servers ──────────────────────────────────────────────────
stop_servers() {
    echo ""
    echo "  Stopping all benchmark servers..."
    if [ -f "$PIDFILE" ]; then
        while read -r pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null
                # Also kill child processes
                pkill -P "$pid" 2>/dev/null
                echo "  Killed PID $pid"
            fi
        done < "$PIDFILE"
        rm -f "$PIDFILE"
    fi
    # Fallback: kill any python processes on known ports
    for port in "${PORTS[@]}"; do
        pid=$(lsof -ti :"$port" 2>/dev/null)
        if [ -n "$pid" ]; then
            kill $pid 2>/dev/null
            echo "  Killed process on port $port (PID $pid)"
        fi
    done
    echo "  Done."
    echo ""
}

# ── Status check ──────────────────────────────────────────────────────
check_status() {
    echo ""
    echo "  ========================================"
    echo "  Benchmark Server Status"
    echo "  ========================================"
    printf "  %-22s %-10s %s\n" "ENVIRONMENT" "STATUS" "PORT"
    echo "  ----------------------------------------"

    for i in "${!NAMES[@]}"; do
        name="${NAMES[$i]}"
        port="${PORTS[$i]}"

        if curl -s --connect-timeout 1 "http://localhost:$port/" > /dev/null 2>&1; then
            printf "  %-22s \033[32m%-10s\033[0m %s\n" "$name" "RUNNING" "$port"
        else
            printf "  %-22s \033[31m%-10s\033[0m %s\n" "$name" "STOPPED" "$port"
        fi
    done
    echo ""
}

# ── Handle arguments ──────────────────────────────────────────────────
case "${1:-start}" in
    stop)
        stop_servers
        exit 0
        ;;
    status)
        check_status
        exit 0
        ;;
    start)
        ;;
    *)
        echo "Usage: $0 [start|stop|status]"
        exit 1
        ;;
esac

# ── Start all servers ─────────────────────────────────────────────────
echo ""
echo "  ========================================"
echo "  Starting Benchmark Servers (10 envs)"
echo "  ========================================"
echo ""

# Clear old pidfile
> "$PIDFILE"

started=0
skipped=0

for i in "${!NAMES[@]}"; do
    name="${NAMES[$i]}"
    cmd="${CMDS[$i]}"
    port="${PORTS[$i]}"

    # Check if already running
    if curl -s --connect-timeout 1 "http://localhost:$port/" > /dev/null 2>&1; then
        echo "  [SKIP] $name — already running on port $port"
        skipped=$((skipped + 1))
        continue
    fi

    # Start in background, redirect output to log
    logfile="$ROOT/logs/server_${name}.log"
    mkdir -p "$ROOT/logs"
    cd "$ROOT"
    $cmd > "$logfile" 2>&1 &
    pid=$!
    echo "$pid" >> "$PIDFILE"

    echo "  [START] $name — port $port (PID $pid)"
    started=$((started + 1))
done

# Wait for servers to bind
echo ""
echo "  Waiting 4 seconds for servers to start..."
sleep 4

# Health check
echo ""
echo "  ── Health Check ──"
healthy=0
failed=0

for i in "${!NAMES[@]}"; do
    name="${NAMES[$i]}"
    port="${PORTS[$i]}"

    if curl -s --connect-timeout 2 "http://localhost:$port/" > /dev/null 2>&1; then
        echo "  [OK]   $name :$port"
        healthy=$((healthy + 1))
    else
        echo "  [FAIL] $name :$port — not responding"
        failed=$((failed + 1))
    fi
done

echo ""
echo "  ========================================"
echo "  Started: $started | Skipped: $skipped | Healthy: $healthy | Failed: $failed"
echo "  ========================================"
echo ""

if [ "$failed" -gt 0 ]; then
    echo "  Check logs in: $ROOT/logs/server_*.log"
    echo ""
fi

echo "  To stop all:    bash start_servers.sh stop"
echo "  To check status: bash start_servers.sh status"
echo ""
