import streamlit as st
from datetime import datetime  # ✅ Add this line
resumed = st.session_state.get("resume_project", None)
import streamlit as st
import base64
import os  
from ai_modules import invitation_generator
import os
import base64
from datetime import datetime   
import tempfile
from PIL import Image, ImageDraw, ImageFont
import os
import math
import os
from multiprocessing import Process
from video_processor import (
    create_invitation_video,
    generate_image_from_prompt,
    load_metadata,
    get_proportional_images
    
)
from PIL import Image
from firebase_utils import save_project, read_projects

os.environ["IMAGEMAGICK_BINARY"] = "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"


from auth import require_login
from components import navbar
resumed = st.session_state.get("resume_project")
require_login()  # 🔐 User must be logged in
navbar.show_navbar()

def apply_fancy_text_style(draw, position, text, font, style="rainbow", frame=0, color="white"):
    x, y = position
    if style == "rainbow":
        colors = [
            (255, 0, 0), (255, 165, 0), (255, 255, 0),
            (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)
        ]
        for i, char in enumerate(text):
            color_cycle = colors[(i + frame) % len(colors)]
            draw.text((x, y), char, font=font, fill=color_cycle)
            x += font.getbbox(char)[2] - font.getbbox(char)[0]
    elif style == "wave":
        for i, char in enumerate(text):
            y_offset = int(5 * math.sin((frame + i) * 0.5))
            draw.text((x, y + y_offset), char, font=font, fill=color)
            x += font.getbbox(char)[2] - font.getbbox(char)[0]
    elif style == "fade":
        alpha = int(255 * (0.5 + 0.5 * math.sin(frame * 0.3)))
        draw.text((x, y), text, font=font, fill=color)
    elif style == "slide-left":
        offset = int(5 * math.sin(frame * 0.3))
        draw.text((x - offset, y), text, font=font, fill=color)
    elif style == "slide-right":
        offset = int(5 * math.sin(frame * 0.3))
        draw.text((x + offset, y), text, font=font, fill=color)
    elif style == "zoom":
        scale = 1 + 0.05 * math.sin(frame * 0.3)
        font_size = int(font.size * scale)
        try:
            zoom_font = ImageFont.truetype("arial.ttf", font_size)
        except:
            zoom_font = font
        draw.text((x, y), text, font=zoom_font, fill=color)
    elif style == "rotate":
        draw.text((x, y), text[::-1] if frame % 2 == 0 else text, font=font, fill=color)
    elif style == "flip":
        draw.text((x, y), text.upper() if frame % 2 == 0 else text.lower(), font=font, fill=color)
    elif style == "pulse":
        brightness = int(128 + 127 * math.sin(frame * 0.3))
        draw.text((x, y), text, font=font, fill=(brightness, brightness, brightness))
    elif style == "shake":
        offset_x = int(3 * math.sin(frame * 2))
        offset_y = int(3 * math.cos(frame * 2))
        draw.text((x + offset_x, y + offset_y), text, font=font, fill=color)
    else:
        draw.text((x, y), text, font=font, fill=color)

# # === Get Position from Keyword or Coordinates ===
def get_position_from_input(position_input, image_size, text_size):
    keywords = {
        "top-left": (20, 20),
        "top-center": ((image_size[0] - text_size[0]) // 2, 20),
        "top-right": (image_size[0] - text_size[0] - 20, 20),
        "center": ((image_size[0] - text_size[0]) // 2, (image_size[1] - text_size[1]) // 2),
        "bottom-left": (20, image_size[1] - text_size[1] - 20),
        "bottom-center": ((image_size[0] - text_size[0]) // 2, image_size[1] - text_size[1] - 20),
        "bottom-right": (image_size[0] - text_size[0] - 20, image_size[1] - text_size[1] - 20)
    }

    if "," in position_input:
        try:
            x, y = map(int, position_input.split(","))
            return (x, y)
        except:
            return (50, 50)
    return keywords.get(position_input.lower(), (50, 50))



# === Create GIF Animation ===
def add_animated_text_box(image_path, output_path, text, font_size=40, position_input="50,50", style="rainbow", font_path="C:/Users/PC-16/Desktop/reel_invitation_creator/assets/fonts/ariali.ttf", text_color="white"):
    if not os.path.exists(image_path):
        print("Image not found.")
        return

    base_image = Image.open(image_path).convert("RGB")
    frames = []
    total_frames = 15

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    try:
        text_width = int(font.getlength(text))
    except:
        text_width = sum(font.getsize(c)[0] for c in text)

    try:
        bbox = font.getbbox(text)
        text_height = bbox[3] - bbox[1]
    except:
        text_height = font.size
    image_size = base_image.size

    for i in range(total_frames):
        frame = base_image.copy()
        draw = ImageDraw.Draw(frame)

        pos = get_position_from_input(position_input, image_size, (text_width, text_height))

        apply_fancy_text_style(draw, pos, text, font, style=style, frame=i, color=text_color)
        frames.append(frame)

    frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0,disposal=2)
    print(f"[✓] Animated GIF saved at: {output_path}")
    return output_path


def overlay_personal_images(bg_path, personal_imgs, text_count):
    if not personal_imgs:
        return [bg_path] * text_count

    distributed_imgs = get_proportional_images(personal_imgs, text_count)
    output_images = []

    for idx, p_img in enumerate(distributed_imgs):
        bg = Image.open(bg_path).convert("RGBA").resize((1280, 720))
        person = Image.open(p_img).convert("RGBA")
        person = person.resize((int(bg.width * 0.4), int(bg.height * 0.4)))

        x = (bg.width - person.width) // 2
        y = (bg.height - person.height) // 2

        bg.paste(person, (x, y), person)

        final_path = os.path.join(tempfile.gettempdir(), f"combined_{idx}_{abs(hash(p_img))}.png")
        bg.save(final_path)
        output_images.append(final_path)

    return output_images
st.set_page_config(page_title="🎨 Create New", page_icon="🎥", layout="wide")
st.title("🎨 Create a New Project")

# ----------------- STEP 1: SELECT PROJECT TYPE -----------------
st.subheader("Step 1: Choose Project Type")

project_type = st.radio(
    "What would you like to create?",
    ["🎥 Reel", "🎉 Invitation","🤖 AI Sample Generation"],
    horizontal=True
)

st.divider()

# ----------------- IF PROJECT TYPE IS INVITATION -----------------
if project_type == "🎉 Invitation":
    st.title("🎉 Fancy Colorful Birthday Invitation Generator")

    if resumed and resumed["type"] == "invitation":
        name = resumed["meta"].get("name", "")
        date = resumed["meta"].get("date", "")
        template_code = resumed["meta"].get("template_type", "p")
        prompt = resumed["meta"].get("prompt", "")
        selected_style = resumed["meta"].get("text_style", "rainbow")
    else:
        name = ""
        date = ""
        template_code = "p"
        prompt = ""
        selected_style = "rainbow"    # ----------------- GENERATE INVITATION ---------------------
    # ----------------- GENERATE INVITATION ---------------------
    with st.form("invitation_form"):
        st.subheader("📄 Basic Details")

        name = st.text_input("👤 Birthday Person's Name", value=name)
        date = st.text_input("📅 Birthday Date (e.g., June 10, 2025)", value=date)

        template_type = st.selectbox(
            "🖼️ Template Type", ["Predefined (p)", "AI Generated (ai)"]
        )
        template_code = "p" if "Predefined" in template_type else "ai"

        uploaded_photo = st.file_uploader("📸 Upload Personal Image", type=["jpg", "png"])

        prompt = st.text_input(
            "✨ AI Prompt for Background (e.g., balloons, cake, confetti)",
            placeholder="balloons, cake, colorful confetti", value=prompt
        )

        st.subheader("🎨 Text Style")
        style_options = {
            "1 - Rainbow": "rainbow",
            "2 - Glow": "glow",
            "3 - 3D Shadow": "3d",
            "4 - Gradient": "gradient",
            "5 - Fire Gradient": "fire",
            "6 - Ocean Gradient": "ocean",
            "7 - Sunset Gradient": "sunset",
            "8 - Mixed Styles": "mixed",
        }
        text_style = st.selectbox("Choose Text Style", list(style_options.keys()))
        selected_style = style_options[text_style]

        submit = st.form_submit_button("✨ Generate Invitation")
    # 🔄 Save as ongoing if basic info is filled
    if st.session_state.user and name and date:
        from datetime import datetime  # ✅ Add this line

        # ✅ Save ongoing project data
        

        user_id = st.session_state.user["localId"]
        project_name = f"Ongoing_Invitation_{name}_{date}".replace(" ", "_")
        ongoing_data = {
            "title": project_name,
            "type": "invitation",
            "status": "ongoing",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "meta": {
                "name": name,
                "date": date,
                "template_type": template_code,
                "prompt": prompt,
                "text_style": selected_style
            },
            "description": f"Ongoing Invitation for {name} on {date}"
        }
        save_project(user_id, project_name, ongoing_data)
    if submit:
        if uploaded_photo is not None:
            with open("uploaded_photo.png", "wb") as f:
                f.write(uploaded_photo.getbuffer())

            with st.spinner("Generating Invitation..."):
                template_path = "assets/templates/generated_3998007689335085946.jpg" if template_code == "p" else "templates/ai_generated.jpg"
                output_path = invitation_generator.generate_birthday_image(
                    name=name,
                    date=date,
                    template_type=template_code,
                    personal_photo_path="uploaded_photo.png",
                    prompt=prompt,
                    text_style=selected_style,
                )

                st.session_state["output_path"] = output_path
                st.session_state["template_path"] = template_path  # ✅ Store globally

                st.success("✅ Invitation Generated Successfully!")
                st.image(output_path, use_column_width=True)

                with open(output_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Invitation",
                        data=file,
                        file_name=f"{name}_invitation.png",
                        mime="image/png",
                    )
        else:
            st.error("❌ Please upload a personal image to continue.")

    # ----------------- EDIT IMAGE ---------------------

    # ----------------- EDIT IMAGE ---------------------
    st.subheader("🛠️ Edit the Image")

    if "output_path" in st.session_state and "template_path" in st.session_state:
        current_output = st.session_state["output_path"]
        template_path = st.session_state["template_path"]

        with st.expander("➕ Click to Edit Position, Size, Text"):
            st.markdown("### 🧭 Image Position and Size")

            st.markdown(
                """
                📍 **Position options:**  
                - Keywords: top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right  
                - Or use coordinates like `250,300`
                """
            )

            position_input = st.text_input(
                "Enter new position for the personal image (keyword or x,y)", value="center"
            )
            size_input = st.text_input(
                "Enter new size for the personal image (width,height)", value="200,200"
            )
            text_position = st.text_input(
                "Enter new text position (auto or keyword like 'top-middle')", value="top-middle"
            )

            # ✅ Process size input
            if size_input:
                try:
                    size = tuple(map(int, size_input.strip().split(",")))
                    if len(size) != 2:
                        raise ValueError
                except:
                    st.error("❌ Invalid size format. Use width,height like 300,400")
                    size = (200, 200)
            else:
                size = (200, 200)

            # ✅ Process position input
            if position_input:
                if "," in position_input:
                    try:
                        x, y = map(int, position_input.strip().split(","))
                        position = (max(0, x), max(0, y))
                    except:
                        st.error("❌ Invalid coordinates. Using default 'center'.")
                        position = "center"
                elif position_input.lower() in [
                    "top-left", "top-center", "top-right",
                    "center-left", "center", "center-right",
                    "bottom-left", "bottom-center", "bottom-right"
                ]:
                    position = position_input.lower()
                else:
                    st.warning("⚠️ Invalid position keyword. Using default 'center'.")
                    position = "center"
            else:
                position = "center"

            # ✅ Handle text position
            if text_position.lower() not in [
                "auto", "top-left", "top-center", "top-right",
                "center-left", "center", "center-right",
                "bottom-left", "bottom-center", "bottom-right"
            ]:
                st.warning("⚠️ Invalid text position. Using 'auto'.")
                text_position = "auto"

            # ✅ Apply changes
            if st.button("Apply Position & Size"):
                edited_path = invitation_generator.edit_generated_image(
                    name=name,
                    date=date,
                    template_path=template_path,  # Load from last output
                    personal_photo_path="uploaded_photo.png",
                    text_pos=text_position,
                    photo_pos=position,
                    new_size=size,
                    text_style=selected_style  # Keep the existing style
                )

                st.session_state["output_path"] = edited_path  # Update for further actions
                st.success(f"✅ Edited image saved at {edited_path}")
                st.image(edited_path, use_column_width=True)

    else:
        st.warning("⚠️ Please generate the invitation first before editing.")


    # ----------------- APPLY EFFECTS ---------------------



    # ----------------- ADD ANIMATED TEXT ---------------------


    st.subheader("🎞️ Add Animated Text")



    if "output_path" in st.session_state:
        current_output = st.session_state["output_path"]

        with st.expander("💫 Animated Text Box"):
            animate = st.radio("Do you want to add animated text?", ["Yes", "No"])

            if animate == "Yes":
                animated_text = st.text_input("Enter text to animate")
                font_size = st.number_input("Font Size", min_value=10, max_value=200, value=50)
                position = st.text_input(
                    "Enter position (x,y or keyword like 'bottom-center')", value="bottom-center"
                )
                animation_type = st.selectbox(
                    "Animation Type",
                    [
                        "color-cycle", "wave", "fade", "slide-left",
                        "slide-right", "zoom", "rotate", "flip", "pulse", "shake"
                    ],
                )
                text_color = st.color_picker("Pick Text Color", "#0000FF")

                if st.button("Generate Animated Text"):
                    if not animated_text:
                        st.error("❌ Please enter text to animate.")
                    else:
                        output_folder = "outputs"
                        os.makedirs(output_folder, exist_ok=True)

                        animated_path = os.path.join(
                            output_folder,
                            f"animated_{os.path.splitext(os.path.basename(current_output))[0]}.gif"
                        )

                        try:
                            result = add_animated_text_box(
                                image_path=current_output,
                                output_path=animated_path,
                                text=animated_text,
                                font_size=font_size,
                                position_input=position,
                                style=animation_type,
                                font_path="C:/Users/PC-16/Desktop/reel_invitation_creator/assets/fonts/ariali.ttf", # Use the correct path for your font
                                
                                text_color=text_color,
                            )

                            if os.path.exists(animated_path):
                                st.session_state["output_path"] = animated_path
                                st.success(f"✅ Animated GIF saved at {animated_path}")

                                with open(animated_path, "rb") as f:
                                    data = base64.b64encode(f.read()).decode("utf-8")
                                    st.markdown(
                                        f'<img src="data:image/gif;base64,{data}" alt="animated gif">',
                                        unsafe_allow_html=True,
                                    )

                                with open(animated_path, "rb") as file:
                                    st.download_button(
                                        label="📥 Download Animated Invitation",
                                        data=file,
                                        file_name="animated_invitation.gif",
                                        mime="image/gif",
                                    )
                            else:
                                st.error("❌ Failed to generate animated text.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
    if "resume_project" in st.session_state:
        del st.session_state["resume_project"]
    else:
        st.warning("⚠️ Please generate the invitation first before adding animation.")
# ----------------- IF PROJECT TYPE IS REEL (COMING SOON) -----------------

elif project_type == "🎥 Reel":

    if resumed and resumed["type"] == "reel":
        name = resumed["meta"].get("name", "")
        age = resumed["meta"].get("age", "")
        date = resumed["meta"].get("date", "")
        time_ = resumed["meta"].get("time", "")
        venue = resumed["meta"].get("venue", "")
        contact = resumed["meta"].get("contact", "")
        rsvp = resumed["meta"].get("rsvp", "")
    else:
        name = age = date = time_ = venue = contact = rsvp = ""

    # ... rest of Reel inputs use value=name, value=date, etc.
# ------------------ Basic Details -------------------
    st.subheader("📄 Basic Details")
    name = st.text_input("👤 Person's Name", value=name)
    age = st.text_input("🎂 Age (optional)", value=age)
    date = st.text_input("📅 Event Date", value=date)
    time_ = st.text_input("⏰ Event Time", value=time_)
    venue = st.text_input("📍 Venue / Address", value=venue)
    contact = st.text_input("📞 Contact Number", value=contact)
    rsvp = st.text_input("✉️ RSVP Name(s)", value=rsvp)

    # ------------------ Text Slides ---------------------
    st.subheader("📝 Text Slides")
    default_text = f"You're Invited to {name}'s Event!"
    text_slides = st.text_area(
        "Enter Text for Each Slide (One per line)",
        f"{default_text}\nOn {date} at {time_}\nAt {venue}\nContact: {contact}\nRSVP: {rsvp}\nThank You!"
    ).splitlines()

    st.divider()

    # ------------------ Background Images ----------------
    st.subheader("🖼️ Background Image Selection")
    bg_type = st.radio("Background Image Type", ["Upload Images", "AI Generated"])

    # Initialize session_state to store AI background images
    if 'ai_backgrounds' not in st.session_state:
        st.session_state['ai_backgrounds'] = []

    background_images = []

    if bg_type == "Upload Images":
        bg_files = st.file_uploader(
            "Upload Background Images", accept_multiple_files=True, type=["jpg", "png"]
        )
        if bg_files:
            for file in bg_files:
                file_path = os.path.join(tempfile.gettempdir(), file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                background_images.append(file_path)

    elif bg_type == "AI Generated":
        prompt = st.text_input("Enter AI Prompt for Background", "Sunset beach, vibrant colors")

        if st.button("Generate AI Background"):
            generated_img = generate_image_from_prompt(prompt)
            st.session_state['ai_backgrounds'].append(generated_img)
            st.image(generated_img, caption="Generated Background", use_container_width=True)

        # Display existing generated backgrounds
        if st.session_state['ai_backgrounds']:
            st.subheader("Generated Backgrounds:")
            for img in st.session_state['ai_backgrounds']:
                st.image(img, use_container_width=True)
                background_images.append(img)

    # ------------------ Personal Photo --------------------
    st.subheader("🧑‍🦰 Personal Photos (Optional)")

    personal_files = st.file_uploader(
        "Upload Personal Images (Optional)", accept_multiple_files=True, type=["jpg", "png"]
    )

    personal_photo_path = []
    if personal_files:
        for file in personal_files:
            file_path = os.path.join(tempfile.gettempdir(), file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            personal_photo_path.append(file_path)

    st.divider()


    # ------------------ Stickers --------------------------
    st.subheader("✨ Stickers (Optional)")
    sticker_files = st.file_uploader("Upload Stickers", accept_multiple_files=True, type=["png"])

    sticker_positions = []
    sticker_sizes = []

    if sticker_files:
        for i, file in enumerate(sticker_files):
            st.markdown(f"**Sticker {i+1}: {file.name}**")
            pos = st.text_input(
                f"Position for Sticker {i+1} (e.g., 'top-left' or '500,200')", "top-right"
            )
            size = st.text_input(
                f"Size for Sticker {i+1} (Width,Height)", "100,100"
            )

            try:
                size_tuple = tuple(map(int, size.split(",")))
            except:
                st.warning("⚠️ Invalid size format, using (100,100).")
                size_tuple = (100, 100)

            if "," in pos:
                try:
                    pos_tuple = tuple(map(int, pos.split(",")))
                except:
                    pos_tuple = ("right", "top")
            else:
                position_map = {
                    "top-left": ("left", "top"),
                    "top-center": ("center", "top"),
                    "top-right": ("right", "top"),
                    "center-left": ("left", "center"),
                    "center": "center",
                    "center-right": ("right", "center"),
                    "bottom-left": ("left", "bottom"),
                    "bottom-center": ("center", "bottom"),
                    "bottom-right": ("right", "bottom"),
                }
                pos_tuple = position_map.get(pos.lower(), ("right", "top"))

            sticker_positions.append(pos_tuple)
            sticker_sizes.append(size_tuple)

    sticker_paths = []
    for file in sticker_files or []:
        path = os.path.join(tempfile.gettempdir(), file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        sticker_paths.append(path)


    # ------------------ Music Upload ----------------------
    st.subheader("🎶 Background Music")
    music_file = st.file_uploader("Upload Background Music (mp3)", type=["mp3"])
    music_path = None
    if music_file:
        music_path = os.path.join(tempfile.gettempdir(), music_file.name)
        with open(music_path, "wb") as f:
            f.write(music_file.getbuffer())


    # ------------------ Other Settings --------------------
    st.subheader("⚙️ Settings")

    animation = st.selectbox("🎈 Animation Overlay", ["None", "balloons", "confetti"])
    slide_duration = st.number_input(
        "Slide Duration (seconds)", min_value=1, max_value=20, value=3
    )
    output_filename = st.text_input(
        "Output Filename (with .mp4)", value="output/reel.mp4"
    )

    # Save as Ongoing if name and date filled
    if st.session_state.user and name and date:
        from firebase_utils import save_project
        user_id = st.session_state.user["localId"]
        project_name = f"Ongoing_Reel_{name}_{date}".replace(" ", "_")

        ongoing_data = {
            "title": project_name,
            "type": "reel",
            "status": "ongoing",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "meta": {
                "name": name,
                "age": age,
                "date": date,
                "time": time_,
                "venue": venue,
                "contact": contact,
                "rsvp": rsvp
            },
            "description": f"Ongoing Reel for {name} on {date}"
        }
        save_project(user_id, project_name, ongoing_data)

    # ------------------ Generate Reel Button ---------------
    if st.button("🎬 Generate Reel"):
        if not text_slides:
            st.error("❌ Please enter at least one text slide.")
        elif not background_images:
            st.error("❌ Please upload background images or generate with AI.")
        else:
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)

            final_background_images = []
            for bg in background_images:
                combined = overlay_personal_images(bg, personal_photo_path, len(text_slides))
                final_background_images.extend(combined)

            proportional_images = get_proportional_images(final_background_images, len(text_slides))

            data = {
                "type": "reel",
                "text_slides": text_slides,
                "images": proportional_images,
                "music_path": music_path if music_path else "",
                "output_filename": output_filename,
                "duration": slide_duration,
                "animation": animation.lower(),
                "sticker_paths": sticker_paths,
                "sticker_positions": sticker_positions,
                "sticker_sizes": sticker_sizes,
            }

            with st.spinner("Generating Reel... Please wait..."):
                try:
                    create_invitation_video(data)
                    st.success(f"✅ Reel saved to {output_filename}")
                    st.video(output_filename)

                    with open(output_filename, "rb") as file:
                        st.download_button(
                            label="📥 Download Reel",
                            data=file,
                            file_name=os.path.basename(output_filename),
                            mime="video/mp4",
                        )
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    
    if "resume_project" in st.session_state:
        del st.session_state["resume_project"]
                    
elif project_type == "🤖 AI Sample Generation":
    st.title("🤖 AI Sample Image Generator")

    # 🔁 Pre-fill if resuming a saved draft
    resumed = st.session_state.get("resume_project")
    if resumed and resumed["type"] == "sample":
        ai_prompt = resumed["meta"].get("prompt", "")
    else:
        ai_prompt = ""

    st.subheader("📝 Enter Text Prompt for Image Generation")
    ai_prompt = st.text_input(
        "Enter a description for the image you want to generate",
        value=ai_prompt,
        placeholder="Example: A futuristic city at night with neon lights"
    )

    # 🔄 Auto-save to Firestore if user is typing a prompt
    from datetime import datetime
    from firebase_utils import save_project

    if st.session_state.user and ai_prompt.strip() != "":
        user_id = st.session_state.user["localId"]
        project_name = f"Ongoing_Sample_{ai_prompt[:25].strip().replace(' ', '_')}"

        ongoing_data = {
            "title": project_name,
            "type": "sample",
            "status": "ongoing",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "meta": {
                "prompt": ai_prompt.strip()
            },
            "description": f"Ongoing AI image generation project with prompt: {ai_prompt[:50]}"
        }

        save_project(user_id, project_name, ongoing_data)

    if st.button("🚀 Generate Image"):
        if ai_prompt.strip() == "":
            st.error("❌ Please enter a valid prompt.")
        else:
            with st.spinner("Generating image... Please wait..."):
                try:
                    generated_image_path = generate_image_from_prompt(ai_prompt)

                    if generated_image_path and os.path.exists(generated_image_path):
                        st.success("✅ Image generated successfully!")
                        st.image(generated_image_path, use_container_width=True)

                        with open(generated_image_path, "rb") as file:
                            st.download_button(
                                label="📥 Download Image",
                                data=file,
                                file_name="ai_generated_sample.png",
                                mime="image/png",
                            )

                        # ✅ Mark project as completed
                        project_name = f"Sample_{ai_prompt[:25].strip().replace(' ', '_')}"
                        completed_data = ongoing_data.copy()
                        completed_data["status"] = "completed"
                        completed_data["meta"]["output_path"] = generated_image_path
                        save_project(user_id, project_name, completed_data)

                        # 🧹 Clear resume project after completion
                        if "resume_project" in st.session_state:
                            del st.session_state["resume_project"]

                    else:
                        st.error("❌ Failed to generate image.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    if "resume_project" in st.session_state:
        del st.session_state["resume_project"]
if "resume_project" in st.session_state:
    del st.session_state["resume_project"]