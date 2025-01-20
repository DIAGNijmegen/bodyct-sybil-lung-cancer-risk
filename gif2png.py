from PIL import Image

def extract_frames(gif_file, output_folder):
    # Open the GIF file
    gif = Image.open(gif_file)

    # Iterate over each frame in the GIF
    for i in range(gif.n_frames):
        # Select the current frame
        gif.seek(i)

        # Convert the frame to RGBA (if it's not already)
        frame = gif.convert("RGBA")

        # Create a new image with a white background
        new_frame = Image.new("RGB", frame.size, (255, 255, 255))
        new_frame.paste(frame, (0, 0), frame)

        # Save the frame as a PNG image
        output_path = f"{output_folder}/frame_{i:03d}.png"
        new_frame.save(output_path, format="PNG")

    # Close the GIF file
    gif.close()


gif_file = ""
output_folder = ""
extract_frames(gif_file, output_folder)
