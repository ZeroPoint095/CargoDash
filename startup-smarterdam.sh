sudo ip link set can0 up type can bitrate 500000
sudo ifconfig can0 txqueuelen 10000

lxterminal --working-directory=$(pwd)/src/ --command="python3 main.py"
lxterminal --working-directory=$(pwd)/src/http_server/ --command="python3 cargo_dash_http_server.py"
lxterminal --working-directory=$(pwd)/src/frontend --command="python3 -m http.server"