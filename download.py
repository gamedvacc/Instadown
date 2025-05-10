import streamlit as st
import instaloader
import os
import shutil

st.set_page_config(page_title="Instagram Video Downloader Only", layout="centered")
st.title("🎥 Instagram Video Downloader (Only Video)")

url = st.text_input("🔗 Enter Instagram Post URL")

def download_video_only(insta_url):
    # Clear old downloads
    if os.path.exists("downloads"):
        shutil.rmtree("downloads")
    os.makedirs("downloads", exist_ok=True)

    # Extract shortcode
    shortcode = insta_url.rstrip("/").split("/")[-1]

    # Initialize Instaloader
    L = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False, download_comments=False)
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    # Check if it's a video
    if post.is_video:
        L.download_post(post, target="")
        # Find video file
        for file in os.listdir("downloads"):
            if file.endswith(".mp4"):
                return os.path.join("downloads", file)
        return None
    else:
        return "NOT_VIDEO"

if url:
    st.info("📥 Checking and downloading video if available...")
    result = download_video_only(url)

    if result == "NOT_VIDEO":
        st.warning("⚠️ This post is not a video. Please provide a video URL.")
    elif result:
        with open(result, "rb") as file:
            st.success("✅ Video ready for download!")
            st.download_button("⬇️ Download Video", file, file_name=os.path.basename(result))
    else:
        st.error("❌ Unable to fetch the video. Make sure the link is public and valid.")
