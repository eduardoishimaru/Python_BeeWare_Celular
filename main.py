import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import datetime
import time
import threading

class AlarmClockApp(toga.App):
    def startup(self):
        # Janela principal
        self.main_window = toga.MainWindow(title=self.name)

        # Variáveis do alarme
        self.alarm_time = None
        self.alarm_status = toga.Label("Alarme não configurado.", style=Pack(padding=10))

        # Relógio
        self.clock_label = toga.Label(self.get_current_time(), style=Pack(font_size=24, padding=10))

        # Botão para configurar alarme
        self.time_input = toga.TextInput(placeholder="HH:MM", style=Pack(padding=10, width=100))
        self.set_alarm_button = toga.Button("Configurar Alarme", on_press=self.set_alarm, style=Pack(padding=10))

        # Layout
        box = toga.Box(
            children=[
                self.clock_label,
                toga.Box(
                    children=[self.time_input, self.set_alarm_button],
                    style=Pack(direction=ROW, padding=10),
                ),
                self.alarm_status,
            ],
            style=Pack(direction=COLUMN, alignment="center", padding=10),
        )

        # Iniciar atualização do relógio
        threading.Thread(target=self.update_clock, daemon=True).start()

        # Configurar e mostrar a janela principal
        self.main_window.content = box
        self.main_window.show()

    def get_current_time(self):
        """Obtém o horário atual como string."""
        return datetime.datetime.now().strftime("%H:%M:%S")

    def update_clock(self):
        """Atualiza o relógio a cada segundo."""
        while True:
            self.clock_label.text = self.get_current_time()
            self.check_alarm()
            time.sleep(1)

    def set_alarm(self, widget):
        """Configura o alarme."""
        alarm_time = self.time_input.value
        try:
            # Validar formato HH:MM
            datetime.datetime.strptime(alarm_time, "%H:%M")
            self.alarm_time = alarm_time
            self.alarm_status.text = f"Alarme configurado para {alarm_time}."
        except ValueError:
            self.alarm_status.text = "Formato de hora inválido. Use HH:MM."

    def check_alarm(self):
        """Verifica se o alarme deve disparar."""
        if self.alarm_time and self.get_current_time()[:5] == self.alarm_time:
            self.alarm_status.text = "⏰ Alarme! Acorde!"
            self.alarm_time = None  # Resetar o alarme

def main():
    return AlarmClockApp("Relógio com Despertador", "org.beeware.alarmclock")
