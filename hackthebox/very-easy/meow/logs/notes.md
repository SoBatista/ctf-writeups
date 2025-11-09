I started by scanning the IP for open ports.
1. I found port 23/tcp - telnet open, and nothing else.
2. Then I tried to connect using telnet to the remote machine (I did not had telnet install, had to do that first...)
3. Once installed I ran the command:
	1. telnet 10.129.47.55 23
	2. I was asked for a Meow login, I tried root (I mean, first try, then it would be admin or even meow!). It was correct, I was in.
4. Once inside, we have a normal root terminal inside the target's VM. I listed the home directory contents, and I saw a file called: flag.txt.
5. Now, how do I get this file into my attacker's system... I didn't want to simply have it copied to clipboard, no, I want to download it!! More fun and realisitc.
6. For this I opened an http server using python3:
	1. python3 -m http.server 8080
		1. This worked, great!
	2. Then I went to my attackers VM, and I simply did:
		1. wget http://10.129.47.55:8080/flag.txt
		2. And I got the file!!
7. All done!

Now to the challenge questions:
1. What does the acronym VM stand for?
	1. Virtual Machine
2. What tool do we use to interact with the operating system in order to issue commands via the command line, such as the one to start our VPN connection? It's also known as a console or shell.
	1. terminal
3. What service do we use to form our VPN connection into HTB labs?
	1. openvpn
4. What tool do we use to test our connection to the target with an ICMP echo request?
	1. ping
5. What is the name of the most common tool for finding open ports on a target?
	1. nmap
6. What service do we identify on port 23/tcp during our scans?
	1. telnet
7. What username is able to log into the target over telnet with a blank password?
	1. root
8. Submit root flag
	1. b40abdfe23665f766f9c61e********
