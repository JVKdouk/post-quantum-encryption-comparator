const fs = require('fs');

const csvHeader = ["name", "key_gen", "cipher_gen", "secret_gen", "data_length", "flight_time", "public_key_size", "cipher_text_size", "secret_key_size", "plaintext_size"].join(';')

function calculate_encapsulation_stats() {
  const data = JSON.parse(fs.readFileSync('./stats/encapsulation.json').toString());
  const stats = data.stats;
  
  const key_gens = stats.filter(entry => entry.label === 'KEY_GENERATION');
  const key_gen_total_time = key_gens.reduce((acc, val) => acc + val.time, 0);
  const key_gen_avg = key_gen_total_time / key_gens.length;

  const cipher_gens = stats.filter(entry => entry.label === 'CIPHER_GENERATION');
  const cipher_total_time = cipher_gens.reduce((acc, val) => acc + val.time, 0);
  const cipher_gen_avg = cipher_total_time / cipher_gens.length;

  const secret_decs = stats.filter(entry => entry.label === 'SECRET_DECRYPTION');
  const secret_total_time = secret_decs.reduce((acc, val) => acc + val.time, 0);
  const secret_dec_avg = secret_total_time / secret_decs.length;
  
  return {
    key_gen: key_gen_avg,
    cipher_gen: cipher_gen_avg,
    secret_gen: secret_dec_avg,
    name: data.algorithm,
    public_key_size: data.public_key_size,
    cipher_text_size: data.cipher_text_size,
    secret_key_size: data.secret_key_size,
    plaintext_size: data.plaintext_size,
  };
}

function calculate_server_stats() {
  const data = JSON.parse(fs.readFileSync('./stats/server.json').toString());
  const stats = data.stats;
  const data_entries = stats.filter(entry => entry.label == 'DATA');

  const data_length = data_entries[0].length;
  const encryption_total_time = data_entries.reduce((acc, val) => acc + val.time, 0);
  const encryption_avg = encryption_total_time / data_entries.length;

  return { data_length: data_length, encryption: encryption_avg };
}

function calculate_client_stats() {
  const data = JSON.parse(fs.readFileSync('./stats/client.json').toString());
  const stats = data.stats;
  const data_entries = stats.filter(entry => entry.label == 'DATA');
  const data_length = data_entries[0].length;

  const encryption_total_time = data_entries.reduce((acc, val) => acc + val.time, 0);
  const encryption_avg = encryption_total_time / data_entries.length;

  return { data_length: data_length, encryption: encryption_avg };
}

function calculate_flight_time() {
  const server_stats = JSON.parse(fs.readFileSync('./stats/server.json').toString()).stats;
  const client_stats = JSON.parse(fs.readFileSync('./stats/client.json').toString()).stats;
  const server_data = server_stats.filter(entry => entry.label == 'DATA');
  const client_data = client_stats.filter(entry => entry.label == 'DATA');

  const flight_times = server_data.map((entry, i) => entry.timestamp - client_data[i].timestamp);
  const total_flight_time = flight_times.reduce((acc, val) => acc + val, 0);
  return { flight_time: total_flight_time / flight_times.length };
}

function append_csv(encapsulation_stats, server_stats, client_stats, flight_stats) {
  if (!fs.existsSync('./results/result.csv')) {
    fs.writeFileSync('./results/result.csv', csvHeader + '\n');
  }

  const data = [
    encapsulation_stats.name,
    encapsulation_stats.key_gen,
    encapsulation_stats.cipher_gen,
    encapsulation_stats.secret_gen,
    client_stats.data_length,
    flight_stats.flight_time,
    encapsulation_stats.public_key_size,
    encapsulation_stats.cipher_text_size,
    encapsulation_stats.secret_key_size,
    encapsulation_stats.plaintext_size,
  ].join(';')

  fs.appendFileSync('./results/result.csv', data + '\n');
}

const encapsulation_stats = calculate_encapsulation_stats();
const server_stats = calculate_server_stats();
const client_stats = calculate_client_stats();
const flight_stats = calculate_flight_time();

append_csv(encapsulation_stats, server_stats, client_stats, flight_stats);
