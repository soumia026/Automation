import { useState } from "react"
import Button from '@mui/material/Button';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import CheckIcon from '@mui/icons-material/Check';
import './main.css'
import * as React from 'react';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Fade from '@mui/material/Fade';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';

function App() {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const [value, setValue] = useState(null);

  const handleChange = (event) => {
    setValue(event.target.value);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const [op, setOp] = useState('Show')
  const [active, setActive] = useState(false)
  const [displayed, setDisplay] = useState(false)
  const [bindings, setBindings] = useState()
  const items = ["Show", "Ping", "DHCP", "VLAN", "NAT","VPN", "OSPF", "SNMP" ]
  const styles = {
    borderRadius: '1.5rem',
    color: 'white',
    backgroundColor: active ? 'green' : '#10afe4',
    alignSelf: 'end',
    '&:hover': {
      backgroundColor: active ? 'green' : '#10afe4',
    },
  };
  const styles1 = {
    borderRadius: '1.5rem',
    color: 'rgb(75 85 99 / var(--tw-text-opacity))',
    backgroundColor: 'transparent',
    padding : '0.5rem 1.25rem',
    border:'4px solid #10afe4',
    alignSelf: 'start',
    '&:hover': {
      backgroundColor: '#10afe4'
    },
  };
  const styles2 = {
    borderRadius: '1.5rem',
    color: 'rgb(75 85 99 / var(--tw-text-opacity))',
    backgroundColor: 'transparent',
    padding : '0.5rem 1.25rem',
    border:'4px solid #10afe4',
    alignSelf: 'end',
    '&:hover': {
      backgroundColor: '#10afe4'
    },
  };
  const handleChange1 = (item)=>{
    setOp(item)
    setActive(false)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      if(op==='DHCP'){
        console.log(value)
        setActive(true)
        const response = await fetch('http://localhost:4000/dhcp/set/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(value),
        });
  
        if (response.ok) {
          const result = await response.json();
          console.log(result)
        } else {
          console.error('Failed to toggle enable');
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };
  const fetchCurrentBindings = async () => {
    try {
      const response = await fetch('http://localhost:4000/dhcp/binding/');

      if (response.ok) {
        const result = await response.json();
        console.log('Current Bindings:', result);
        setBindings(result)
        setDisplay(true)
        console.log(bindings)
      } else {
        console.error('Failed to fetch current bindings');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className=" w-screen h-screen bg-[#B3C8CF] flex items-center justify-center">
      <div className="flex flex-col md:grid md:grid-rows-6 md:grid-cols-1 p-4 w-5/6 h-5/6 border-2 rounded-3xl bg-white/25 backdrop-blur-md">
        <span className="col-span-2 row-span-2 flex flex-col items-center justify-center ">
          <p >welcome to</p>
          <span className="text-7xl  font-bold bg-gradient-to-r from-[#76cddf] via-[#13a2b5] to-[#10afe4]   text-transparent bg-clip-text font-northStar">SHABAKA</span>
          <p>where you can configure, manage and monitor your network!</p>
        </span>
        <div className="flex row-span-4 w-2/3 flex-col justify-self-center self-start items-center justify-center gap-6 px-2">
          <ul className="flex justify-around rounded-[2rem] w-full  border-4 border-[#10afe4]">
            { 
              items.map((item, index)=>(
                <li
                  key={index}
                  className={`cursor-pointer py-3 w-full text-center rounded-3xl ${op === item ? 'bg-[#10afe4] text-white px-4' : 'bg-transparent text-gray-600'}`}
                  onClick={() => handleChange1(item)
                  }
                >{item}
                </li>
              ))
            }
          </ul>
          <p className="text-xs text-gray-600 self-start"> * please note that when you enable DHCP, all devices in that network will be automatically configured</p>
          
          <Button
        id="fade-button"
        aria-controls={open ? 'fade-menu' : undefined}
        aria-haspopup="true"
        aria-expanded={open ? 'true' : undefined}
        onClick={handleClick}
        sx={styles1}
        className='self-start   rounded-3xl hover:bg-[#10afe4]  hover:text-white border-4 py-2 px-5 border-[#10afe4] text-gray-600'
      >
        Enable / Disable
      </Button>
        <Menu
          id="fade-menu"
          MenuListProps={{
            'aria-labelledby': 'fade-button',
          }}
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          TransitionComponent={Fade}
        >
          <RadioGroup
            aria-labelledby="fade-button"
            name="controlled-radio-buttons-group"
            value={value}
            onChange={handleChange}
          >
          <MenuItem>
              <FormControlLabel value="" control={<Radio />} label="none" />
            </MenuItem>
            <MenuItem>
              <FormControlLabel value="Router1" control={<Radio />} label="Router 1" />
            </MenuItem>
            <MenuItem>
              <FormControlLabel value="Router4" control={<Radio />} label="Router 4" />
            </MenuItem>
          </RadioGroup>
        </Menu>
        <Button variant="outlined" startIcon={active ? <CheckIcon/> : <ArrowCircleUpIcon />}
          sx={styles}
          onClick={handleSubmit}>
            {active ? 'activated' : 'activate'}
          </Button>
        <Button
        aria-haspopup="true"
        onClick={fetchCurrentBindings}
        sx={styles2}
        className=' hover:bg-[#10afe4]  hover:text-white border-4 py-2 px-5 border-[#10afe4] text-gray-600'
      >
         Display current bindings
      </Button>

        </div>
      </div>
    </div>
  )
}

export default App