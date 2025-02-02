from whad.device import WhadDevice
from whad.ble.connector import Central
from whad.ble.profile.device import PeripheralDevice
import random
from scapy.layers.bluetooth import ATT_Prepare_Write_Request

def mutate_fill_payload(att_proc, gatt_handle):
    match att_proc:
        case scapy.layers.bluetooth.ATT_Prepare_Write_Request:
            _gatt_handle = random.choice(gatt_handle)
            _offset = random.randint(0, 65535)
            n = random.randint(0, 80)
            _data = random.randbytes(n)
            return ATT_Prepare_Write_Request(gatt_handle=_gatt_handle, 
                                             offset=_offset, 
                                             data=_data), 5 + n

# 创建WhadDevice对象，使用默认的蓝牙适配器
device = WhadDevice.create('hci0')

# 创建Central对象，传递WhadDevice对象
central = Central(device=device)

# 连接到目标设备
target_bd_address = '20:91:48:6B:65:08'
peripheral = central.connect(target_bd_address)

# 发现服务和特性
peripheral.discover()

# 发送模糊测试请求
for _ in range(1000):
    payload, length = mutate_fill_payload(scapy.layers.bluetooth.ATT_Prepare_Write_Request, [0x0010])
    peripheral.writeCharacteristic(payload.handle, payload.value)

# 断开连接
peripheral.disconnect()
