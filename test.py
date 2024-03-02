test_A =   {"monitor": {
                "cpu": {
                    "cpu1_5s": "0",
                    "cpu2_5s": "0",
                    "cpu1_1m": "0",
                    "cpu1_5m": "0"
                }
            }
}

test_B = {"monitor": {
            "cpu": {
                "cpu0": {
                    "cpu_current": "5%",
                    "cpu_5sec": "0%",
                    "cpu_1min": "0%",
                    "cpu_5min": "0%"
                },
                "cpu1": {
                    "cpu_current": "2%",
                    "cpu_5sec": "0%",
                    "cpu_1min": "0%",
                    "cpu_5min": "0%"
                }
            }
        }
}

def test(data):
    for cpu_name in data["monitor"]:
        lv1_data = data["monitor"][cpu_name]
        final_data = lv1_data
        for lv2_key in lv1_data:
            lv2_data = lv1_data[lv2_key]
            if type(lv2_data) != str:
                final_data = lv2_data
                cpu_proc(ip, final_data)
            else:
                cpu_proc(ip, final_data)
                break
        # cpu_proc(ip, final_data)


test(test_B)