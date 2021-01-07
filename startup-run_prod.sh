sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

gnome-terminal --working-directory=$(pwd)/src/ --command="python3 main.py"
gnome-terminal --working-directory=$(pwd)/src/http_server/ --command="python3 cargo_dash_http_server.py"
gnome-terminal --working-directory=$(pwd)/src/frontend --command="python3 -m http.server"