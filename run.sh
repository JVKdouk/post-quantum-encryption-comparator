python encapsulation.py
python generate_keys.py

python server.py &
sleep 1s
python client.py &
wait

node tools/convert.js