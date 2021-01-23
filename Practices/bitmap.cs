using System;
using System.IO;

public class EmptyClass
{
    #region Settings

    static string filename = "pruba.ppm";

    static int width = 1500;
    static int height = 400;

    static int stripeWidth = width / 30;
    static rgb stripeLowCol = new rgb(204, 0, 0);
    static rgb stripeHighCol = new rgb(255, 51, 51);

    static float multiplier = 1f;

    #endregion

    #region Image Generator

    public static void Main()
    {
        byte[] pixelData = new byte[width * height * 3];
        for(int x = 0; x < width; ++x)
        {
            for(int y = 0; y < height; ++y)
            {
                int currentPixel = ((y * width) + x) * 3;
                pixelData[currentPixel] = redPixel(x, y);
                pixelData[currentPixel + 1] = greenPixel(x, y);
                pixelData[currentPixel + 2] = bluePixel(x, y);
            }
        }

        StreamWriter destination = new StreamWriter(filename);
        destination.Write("P6\n{0} {1}\n{2}\n", width, height, 255);
        destination.Flush();
        destination.BaseStream.Write(pixelData, 0, pixelData.Length);
        destination.Close();
    }

    #endregion

    #region Pixel value functions - edit these

    public static byte redPixel(int x, int y)
    {
        return (byte)(((x + y) % stripeWidth < stripeWidth / 2 ? stripeLowCol.r : stripeHighCol.r) * multiplier);
    }
    public static byte greenPixel(int x, int y)
    {
        return (byte)(((x + y) % stripeWidth < stripeWidth / 2 ? stripeLowCol.g : stripeHighCol.g) * multiplier);
    }
    public static byte bluePixel(int x, int y)
    {
        return (byte)(((x + y) % stripeWidth < stripeWidth / 2 ? stripeLowCol.b : stripeHighCol.b) * multiplier);
    }

    #endregion
}

#region Utility Classes
class rgb
{
    public byte r, g, b;
    public rgb(byte inCol)
    {
        r = g = b = inCol;
    }
    public rgb(byte inR, byte inG, byte inB)
    {
        r = inR;
        g = inG;
        b = inB;
    }
}
#endregion