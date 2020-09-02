import React, {Component} from 'react';
import {Auth} from 'aws-amplify';

class SignUpForm extends Component{
    constructor(props){
        super(props);
        this.state={
            username:'',
            password:'',
            email:'',
            phone_number:'',
            signedUp: false

        }
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(e){
        e.preventDefault();
        cost {signedUp, username,password,email, phone_number} = this.state;

        if(signedUp){
            Auth.signUp({
                username : username,
                password: password,
                attributes: {
                    email: email,
                    phone_number: phone_number
                }
            })
            .then(() => console.log('signed up'))
            .catch(err => console.log(err));
            this
        }


        Auth.signUp({
            username : username,
            password: password,
            attributes: {
                email: email,
                phone_number: phone_number
            }
        })
        .then(() => console.log('signed up'))
        .catch(err => console.log(err));
    }

    handleChange(e){
        this.setState({[e.target.name]: e.target.value});
    }

    render(){
        const {signedUp} = this.state;
        if(signedUp){

        } else{
            return(
                <form onSubmit={this.handleSubmit}>
                    <label>Username</label>
                    <input type='text' name='username' onChange={this.handleChange}/>
                    <label>Password</label>
                    <input type='password' name='password'onChange={this.handleChange}/>
                    <label>Email</label>
                    <input type='text' name='email'onChange={this.handleChange}/>
                    <label>Phone Number</label>
                    <input type='text' name='phone_number'onChange={this.handleChange}/>
                    <button>Sign up</button>
                    
                 </form>   
            )
        }
    }
}

export default SignUpForm;