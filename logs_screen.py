from extronlib.device import UIDevice
from extronlib.ui import Label

logs_to_text = True

WebGUI = UIDevice('WebGUI')  # WEbUI alias name
log_list = []
max_logs = 36

def custom_logger(incoming_data1, incoming_data2=None, incoming_data3=None):
    global log_list
    global max_logs
    if incoming_data2 is None:
        if incoming_data3 is None:
            log_list.append(str(incoming_data1))
    else:
        if incoming_data3 is None:
            log_list.append("{} {}".format(str(incoming_data1), str(incoming_data2)))
        else:
            log_list.append("{} {} {}".format(str(incoming_data1), str(incoming_data2), str(incoming_data3)))
    
    # Проверяем, превышает ли количество логов максимальное значение
    if len(log_list) > max_logs:
        # Удаляем старые логи
        del log_list[0:len(log_list)-max_logs]

def update_logs():
    global log_list
    num_labels = 6
    label_id = 279
    label_components = [Label(WebGUI, label_id + i) for i in range(num_labels)]

    try:
        for i, label_component in enumerate(label_components):
            start_index = i * 6
            end_index = start_index + 6

            if start_index >= len(log_list):
                break

            log_text = "\n".join(log_list[start_index:end_index])
            label_component.SetText(log_text)

    except Exception as e:
        print("Произошла ошибка при обновлении логов")
