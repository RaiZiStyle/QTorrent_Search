from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
from pathlib import Path
from ssl import create_default_context


class EmailSender:
    def __init__(self, path_token: Path = Path("token.txt")) -> None:
        super().__init__()
        self.username = "raizystyle.dev@gmail.com"
        with open(path_token, "rb") as f:
            self.password = f.read().decode("utf-8")
        self.message = MIMEMultipart("alternative")
        self.message["From"] = "raizystyle.dev@gmail.com"
        self.message["To"] = "raizystyle.dev@gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.ctx = create_default_context()

    def sendmail(self,
                 attachement: str = False,
                 subject: str = "Default Subject",
                 message: str = "Default message"):
        self.message["Subject"] = subject
        self.message.attach(MIMEText(message, "plain"))

        if attachement:
            print("Attaching file to msg")
            try:
                with open(attachement, "rb") as f:
                    file = MIMEApplication(f.read())
            except FileNotFoundError as e:
                print(f"FileNotFoundError successfully handled\n"f"{e}")
            except Exception as e:
                print(f"An exception occur : {e}")

            disposition = f"attachment; filename={attachement}"
            file.add_header("Content-Disposition", disposition)
            self.message.attach(file)

        with smtplib.SMTP_SSL(self.smtp_server,
                              port=self.smtp_port,
                              context=self.ctx) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, self.username, self.message.as_string())


if __name__ == '__main__':
    MyEmailSender = EmailSender()
    MyEmailSender.sendmail()
