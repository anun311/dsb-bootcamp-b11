#!/usr/bin/env python
# coding: utf-8

# # Scraping TikTok Live Data

# In[47]:


# ปลดคอมเม้นต์เพื่อติดตั้ง Library TikTokLive
# !pip install TikTokLive


# In[63]:


import asyncio  # Import asyncio


# In[49]:


from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, RoomUserSeqEvent


# In[51]:


client: TikTokLiveClient = TikTokLiveClient(unique_id="@bemeclinic")


# In[53]:


@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}")


# In[55]:


# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    print(f"{event.user.nickname} -> {event.comment}")


# In[57]:


client.add_listener(CommentEvent, on_comment)


# In[59]:


@client.on(CommentEvent)
async def on_connect(event: CommentEvent):
    print(f"{event.user.unique_id} -> {event.comment}")


# In[ ]:


@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    global running  # Access the global running flag
    if running: # Only process comments if running is True
        like_.append({
            "user_id": event.user.unique_id,
            "like_count": event.likeCount
        })
        print(f"{event.user.unique_id} has liked the stream {event.likeCount} times, thre is now {event.totalLikeCount} total likes")


# In[ ]:




