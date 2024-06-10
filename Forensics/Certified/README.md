# Forensics: Certified (100)

One of our machines was recently hit with malware and appears to have opened a backdoor. We were able to get this PCAP from around the time when it was accessed but aren't sure what was exfiltrated from the network. Take a look and see if you can make sense of it!

Author: [tsuto](https://github.com/jselliott)

In this challenge, we are given a PCAP file. First, we need to open in Wireshark.

When we do, we see first some HTTP traffic and then TLS traffic. However, we also see in the request to `/backdoor.php` an RSA key which is very helpful!

![Image 1](Screenshots/1.png)

Copying the value of the first HTTP body and decoding the hexadecimal, we get the key:

```
-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----
```

We can write this to a file and then load it into Wireshark.

To load it, we go to Edit > Preferences > Protocols > TLS, and then click to edit the RSA keys list. 

![Image 2](Screenshots/2.png)

After we do this, we see some HTTP traffic! Particularly, the response gives something interesting:

![Image 3](Screenshots/3.png)

And now, although we aren't Agent J, we have the code/flag to access the mainframe: `SIVUSCG{c3rtif1abl3_h4ck3rs}`!

