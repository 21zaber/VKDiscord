# VKDiscord
Integration between VK group/public and discord channel.

# Instalation 
```
 $ sudo apt install python3 python3-pip
 $ pip3 install requests flask 
 $ chmod +x vkdiscord.py
```

# Config
 > "vk_group_id"          - ID of your VK group 
 > "vk_confirmation_code" - confirmation code from VK (more information about [VK Callback API](https://vk.com/dev/callback_api))
 > "discord_webhook_url"  - Discord Webhook URL (more information about [Discord Webhooks](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks))

# Run
```
  ./vkdiscord.py
```
   
# See also
discord_hooks.py created by [4rqm](https://github.com/4rqm/dhooks)



