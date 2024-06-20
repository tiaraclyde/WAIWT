import React from 'react'
import {useState} from 'react'


function LogIn() {
const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  return (
    <>
    <div className="w-50 mx-auto">
    <div className="mb-3">
    <label for="exampleFormControlInput1" class="form-label">Email address</label>
    <input type="email" className="form-control" id="exampleFormControlInput1" placeholder="name@example.com" value={email} onChange={(e)=> {setEmail(e.target.value)}}/>
  </div>
  <div className="mb-3">
  <label for="inputPassword5" class="form-label">Password</label>
<input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" value={password} onChange={(e)=> {setPassword(e.target.value)}}/>
  </div>
  <button type="button" class="btn btn-primary" onClick={() => {console.log(email,password)}}>Log In</button>
  </div>
    </>
  )
}

export default LogIn