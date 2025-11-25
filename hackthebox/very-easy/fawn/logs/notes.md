I started by scanning the IP for open ports.
1. I found port 21/tcp - ftp open, and I also noticed that anonymous was enable, and there was a file inside, flag.txt.
2. Then I tried to connect using ftp to the remote machine (I did not had ftp installed, had to do that first...)
3. Once installed I ran the command:
	1. ftp 10.129.102.11
	2. I was asked for a name, I tried anonymous (I mean, it was open according to nmap scan).
	3. Then I got prompted for a password. After reading a bit the documentation for ftp (and also from previous challenges) I knew that for anonymous the default password is ... nothing! Empty password, so I just pressed enter, and I was in.
4. Once inside, we have a normal ftp terminal. I listed the home directory contents, and I saw a file called: flag.txt.
5. Now, how do I get this file into my attacker's system... A quick search on ftp, and I found the command get <file_name> that would allow me to download the file to my local system, so I ran: 
	ftp flag.txt
	and the file was promptly donwloaded
6. I exited ftp, and I did a simple cat of the flag.txt file, there it was the flag.
7. All done!

Now to the challenge questions:
1. What does the 3-letter acronym FTP stand for?
	* File Transfer Protocol
2. Which port does the FTP service listen on usually?
	* 21
3. FTP sends data in the clear, without any encryption. What acronym is used for a later protocol designed to provide similar functionality to FTP but securely, as an extension of the SSH protocol?
	* SFTP
4. What is the command we can use to send an ICMP echo request to test our connection to the target?
	* ping
5. From your scans, what version is FTP running on the target?
	* vsftpd 3.0.3
6. From your scans, what OS type is running on the target?
	* Unix
7. What is the command we need to run in order to display the 'ftp' client help menu?
	* ftp -?
8. What is username that is used over FTP when you want to log in without having an account?
	* anonymous
9. What is the response code we get for the FTP message 'Login successful'?
	* 230
10. There are a couple of commands we can use to list the files and directories available on the FTP server. One is dir. What is the other that is a common way to list files on a Linux system.
	* ls
11. What is the command used to download the file we found on the FTP server?
	* get
12. Submit root flag
	* 035db21c881520061c53e05********
