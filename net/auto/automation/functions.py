import telnetlib3
import asyncio

# async def set_ip_for_int(host, port, ip, gateway):
#     try:
#         reader, writer = await telnetlib3.open_connection(host=host, port=int(port))
#     except Exception as e:
#         return f"Error when establishing connection with device: {e}"

#     try:
#         # Writing configuration commands
#         writer.write('configure terminal\r')
#         await asyncio.sleep(1)
#         writer.write('interface Serial1/1\r')
#         await asyncio.sleep(1)
#         writer.write(f'ip address {ip} 255.255.255.0\r')
#         await asyncio.sleep(1)
#         writer.write('exit\r')
#         await asyncio.sleep(1)
#         writer.write('write memory\r')
#         await asyncio.sleep(1)

#         # Closing the connection
#         writer.write('exit\r')
#         await writer.drain()
#         writer.close()
#         await asyncio.sleep(1)  # Give it a moment to close
#         return f"{ip} was assigned successfully."
#     except Exception as e:
#         return f"An error occurred: {e}"

# async def set_ip_for_pc(host, port, ip, gateway):
#     try:
#         reader, writer = await telnetlib3.open_connection(host=host, port=int(port))
#     except Exception as e:
#         return f"Error when establishing connection with device: {e}"

#     try:
#         writer.write(f"ip {ip} 255.255.255.0 {gateway}\r")
#         await writer.drain()
#         await asyncio.sleep(1)

#         writer.write("wr\r")
#         await writer.drain()
        
#         res = await reader.read(4096)  # Read the response

#         if "MAC" in res:
#             return "IP address already taken"
#         if "Invalid address" in res:
#             return "Invalid IP address"
#         if "Invalid gateway address" in res:
#             return "Invalid gateway address"
#         if "Checking for duplicate address..." in res:
#             return f"{ip} was assigned successfully"
#         return "Something went wrong, please try again"
#     finally:
#         writer.close()
#         await writer.wait_closed()

async def set_dhcp(router):
   if router == "Router1":
        port = 5000
        ip_int = "192.168.1.1"
        network = "192.168.1.0"
        subnet_mask = "255.255.255.0"
        default_router = "192.168.1.10"
    else:
        port = 5003
        ip_int = "192.168.4.1"
        network = "192.168.4.0"
        subnet_mask = "255.255.255.0"
        default_router = "192.168.4.10"


    try:
        reader, writer = await telnetlib3.open_connection(host="localhost", port=int(port))
    except Exception as e:
        return f"Error when establishing connection with {router}: {e}"

    try:
        # Configure DHCP settings on interface
        writer.write("configure terminal\r")  
        await writer.drain()
        await asyncio.sleep(1)

        # Configure interface
        writer.write("interface FastEthernet0/0\r")  
        await writer.drain()
        await asyncio.sleep(1)

        # Set IP address and subnet mask
        writer.write(f"ip address {ip_int} {subnet_mask}\r")  
        await writer.drain()
        await asyncio.sleep(1)

        # Activate the interface
        writer.write("no shutdown\r")
        await writer.drain()
        await asyncio.sleep(1)

        # Exit interface configuration mode
        writer.write("exit\r")
        await writer.drain()
        await asyncio.sleep(1)

        # Exclude IP address from DHCP pool
        writer.write(f"ip dhcp excluded-address {ip_int}\r")  
        await writer.drain()
        await asyncio.sleep(1)

        # Configure DHCP pool
        writer.write("ip dhcp pool MYPOOL\r")
        await writer.drain()
        await asyncio.sleep(1)

        # Set network and default router for DHCP pool
        writer.write(f"network {network} {subnet_mask}\r")  
        await writer.drain()
        await asyncio.sleep(1)

        writer.write(f"default-router {default_router}\r")  
        await writer.drain()
        await asyncio.sleep(1)

        # Exit DHCP pool configuration mode
        writer.write("end\r")
        await writer.drain()
        await asyncio.sleep(1)

        # Save configuration
        writer.write("write memory\r")
        await writer.drain()
        await asyncio.sleep(2)

        # Read the response
        response = await reader.read(4096)

        # Conditional checks for additional commands based on router port
        additional_ports = []
        if port == 5000:
            additional_ports = [5008, 5015, 5020]  # PC1, PC2, PC3 ports
        elif port == 5003:
            additional_ports = [5014, 5016]  # PC4, PC5 ports

        for pc_port in additional_ports:
            try:
                pc_reader, pc_writer = await telnetlib3.open_connection(host="localhost", port=int(pc_port))
                pc_writer.write("ip dhcp\r")
                await pc_writer.drain()
                await asyncio.sleep(1)
                pc_writer.write("save myconfig.vpc\r")
                await pc_writer.drain()
                await asyncio.sleep(1)
                pc_writer.close()
            except Exception as e:
                return f"Error when executing commands on PC connected to port {pc_port}: {e}"

        return f"{router} DHCP configuration applied successfully."

    finally:
        writer.close()

async def get_dhcp_binding(port):
    try:
        reader, writer = await telnetlib3.open_connection(host="localhost", port=int(port))
    except Exception as e:
        return f"Error when establishing connection: {e}"

    try:
        # Send the command to get DHCP bindings
        writer.write("show ip dhcp binding\r")
        await writer.drain()
        await asyncio.sleep(1)

        # Read the response
        response = await reader.read(4096)
        
        # Process the response to format it similarly to the original function
        res = []
        tmp = response.split('\r\n')[-2::-1]
        for i in tmp:
            if '#' in i:
                break
            res.insert(0, i)
        
        return '\n'.join(res)

    finally:
        writer.close()      