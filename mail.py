import tkinter as tk
from tkinter import messagebox
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an email
def send_email():
    try:
        sender_email = email_entry.get()
        sender_password = password_entry.get()
        receiver_email = receiver_entry.get()
        subject = subject_entry.get()
        message = message_text.get("1.0", "end")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, receiver_email, msg.as_string())
        smtp_server.quit()

        messagebox.showinfo("Success", "Email sent successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to receive emails
def receive_emails():
    try:
        receiver_email = email_entry.get()
        receiver_password = password_entry.get()

        imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
        imap_server.login(receiver_email, receiver_password)
        imap_server.select('inbox')

        _, data = imap_server.search(None, 'ALL')
        email_ids = data[0].split()

        for email_id in email_ids:
            _, message_data = imap_server.fetch(email_id, '(RFC822)')
            msg = message_data[0][1].decode('utf-8')
            received_emails.insert(tk.END, msg)

        imap_server.logout()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Email Client")

# Email and password input fields
email_label = tk.Label(root, text="Email:")
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Receiver email, subject, and message input fields
receiver_label = tk.Label(root, text="Receiver Email:")
receiver_label.pack()
receiver_entry = tk.Entry(root)
receiver_entry.pack()

subject_label = tk.Label(root, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

message_label = tk.Label(root, text="Message:")
message_label.pack()
message_text = tk.Text(root)
message_text.pack()

# Send and receive buttons
send_button = tk.Button(root, text="Send Email", command=send_email)
send_button.pack()

receive_button = tk.Button(root, text="Receive Emails", command=receive_emails)
receive_button.pack()

# Listbox to display received emails
received_emails = tk.Listbox(root, width=50, height=10)
received_emails.pack()

root.mainloop()
