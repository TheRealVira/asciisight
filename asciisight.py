import argparse, vtkplotlib, math, vtk, getch
from stl.mesh import Mesh
from PIL import Image

getch = getch._Getch()

# ASCII grayscale pixels (inverted)
colorRamp = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
colorRampLength = len(colorRamp)

currentkey = " "

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rendering your STL files in 2D ASCII art!"
    )
    parser.add_argument("filelocation", help="File location.")
    parser.add_argument('-s', '--size', help="ASCII image size.", default=120, type=int)
    
    args = parser.parse_args()
    file_location = args.filelocation
    size = args.size
    
    # pipe vtk output errors to file to stop any annoying vtk warning windows from popping up...
    errOut = vtk.vtkFileOutputWindow()
    errOut.SetFileName("VTK Error Out.txt")
    vtkStdErrOut = vtk.vtkOutputWindow()
    vtkStdErrOut.SetInstance(errOut)
    
    # Load stl
    mesh = Mesh.from_file(file_location)
    vtkplotlib.mesh_plot(mesh)
    fig = vtkplotlib.gcf()
    fig.background_color = "black"
    
    while currentkey in "wasdWASD ":
        # Clear screen
        print("\033[H\033[J", end="")
        
        # Recalculate position
        if currentkey in "Aa":
            fig.camera.Yaw(10)
        elif currentkey in "Dd":
            fig.camera.Yaw(-10)
        if currentkey in "Ww":
            fig.camera.Pitch(10)
        elif currentkey in "Ss":
            fig.camera.Pitch(-10)
        
        fig.reset_camera()
        
        # Render new image
        img = Image.fromarray(vtkplotlib.screenshot_fig(magnification=1, pixels=(size,size), trim_pad_width=1, off_screen=True, fig=fig))
        width, height = img.size
        pixels = ''.join([colorRamp[math.ceil((colorRampLength-1) * pixel / 255)] for pixel in img.resize((size, int((height/width) * size * 0.55))).convert('L').getdata()])
        ascii_image = "\n".join([pixels[index:index + size] for index in range(0, len(pixels), size)])
        
        # Print key info and wait for a new button press
        print(f'{ascii_image}\n\nPress WASD to rotate the model and any other key to quit...')
        currentkey = getch().decode()