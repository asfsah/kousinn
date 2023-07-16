import PySimpleGUI as sg
import requests
import datetime
import time
import os
import ctypes
import platform
import socket
import wmi

def get_hwid():
    c = wmi.WMI()
    system_info = c.Win32_ComputerSystemProduct()[0]
    return system_info.UUID.lower()

hwid = get_hwid()
host = socket.gethostname()

sg.theme('DarkGrey1')

def get_hwid():
    if platform.system() == 'Windows':
        volume_serial_number = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(os.path.abspath("C:\\")),
            None,
            None,
            ctypes.pointer(volume_serial_number),
            None,
            None,
            None,
            None
        )
        return str(volume_serial_number.value)
    else:
        return None

layout = [
    [sg.Text('選択してください:')],
    [sg.InputCombo(['ログイン', '1ヶ月', '3ヶ月', '5ヶ月', '1年', '永久'], size=(20, 6), key='-CHOICE-')],
    [sg.Button('OK'), sg.Button('キャンセル')]
]

window = sg.Window('セットアップ', layout, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'キャンセル':
        window['-CHOICE-'].update(value='')
        break
    elif event == 'OK':
        selected_choice = values['-CHOICE-']
        window.close()

        if selected_choice == 'ログイン':
            key_pass = {
                '111': {'password': '333', 'hwid': '808C1F4E-B59D-E511-8061-B0EDA6045094'}
            }

            layout_login = [
                [sg.Text('キー:')],
                [sg.Input(key='-KEY-', password_char='*')],
                [sg.Text('パスワード:')],
                [sg.Input(key='-PASSWORD-', password_char='*')],
                [sg.Button('ログイン'), sg.Button('キャンセル')]
            ]

            window_login = sg.Window('ログイン', layout_login)

            while True:
                event_login, values_login = window_login.read()
                if event_login == sg.WINDOW_CLOSED or event_login == 'キャンセル':
                    window_login.close()
                    break
                elif event_login == 'ログイン':
                    key = values_login['-KEY-']
                    password = values_login['-PASSWORD-']
                    if key in key_pass and password == key_pass[key]['password']:
                        hwid = get_hwid()
                        if hwid is not None and hwid.lower() == key_pass[key]['hwid'].lower():
                            sg.popup('ログインに成功しました', title='ログイン成功')
                            window_login.close()
                            os.system('python mhe.py')
                            break
                        else:
                            sg.popup('HWIDの認証に失敗しました', title='ログイン失敗')
                            window_login.close()
                            break
                    else:
                        sg.popup('ログインに失敗しました', title='ログイン失敗')

        else:
            layout_additional = [
                [sg.Text('Discordユーザーネーム:')],
                [sg.Input(key='-DISCORD-')],
                [sg.Text('メールアドレス:')],
                [sg.Input(key='-EMAIL-')],
                [sg.Button('送信'), sg.Button('キャンセル')]
            ]

            window_additional = sg.Window('追加情報入力', layout_additional)

            while True:
                event_additional, values_additional = window_additional.read()
                if event_additional == sg.WINDOW_CLOSED or event_additional == 'キャンセル':
                    window_additional.close()
                    break
                elif event_additional == '送信':
                    discord_username = values_additional['-DISCORD-']
                    email = values_additional['-EMAIL-']

                    webhook_url = 'https://discord.com/api/webhooks/1129777803009728659/F5ZRE-LEPHqIExUtjOIVtrB5MObHSmIKinHDbWTCawe42btYleE2OYNvl5hB2_uG9d8Z'

                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    message = f"{current_time} : subscription plan : \"**{selected_choice}**\" hwid : \"**{hwid}**\" discord : \"**{discord_username}**\" ip : \"**{socket.gethostbyname(host)}**\" username : \"**{email}**\""

                    payload = {
                        'content': message
                    }
                    response = requests.post(webhook_url, json=payload)
                    if response.status_code == 204:
                        sg.popup('お申し込みに成功しました！\n1 ~ 2日以内に指定したDiscordユーザーネームにDMが来ると思います！\nもし、DM等が送れなかった場合はメールにライセンスキーを発行いたします！', title='完了')
                    else:
                        sg.popup('メッセージの送信に失敗しました', title='エラー')

                    break

            window_additional.close()

window.close()
