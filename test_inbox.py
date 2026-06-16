import smtplib

server = smtplib.SMTP("mail.datapowered.tech", 587)
server.starttls()

server.login(
    "agent@datapowered.tech",
    "ptjis9EUcFcnCpL"
)

print("Success")
server.quit()