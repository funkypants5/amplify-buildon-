  
import React, { Component } from 'react';
import { withAuthenticator, AmplifySignOut } from '@aws-amplify/ui-react';
//import {withAuthenticator} from 'aws-amplify-react';
import Particles from 'react-particles-js';


import awsconfig from './aws-exports';
import './App.css';
import aws_exports from './aws-exports';


Amplify.configure(aws_exports);
Amplify.configure(awsconfig);
Amplify.configure({
  Auth: {
    identityPoolId: 'us-east-1:6021490f-2e8e-4b46-a341-d6cc37c2ad61',
    region: 'us-east-1'
  },
  
});

Storage.configure({
customPrefix: {public:''}
})

// Imported default theme can be customized by overloading attributes
const myTheme = {
  ...AmplifyTheme,
  color:'#00f0fc',
  sectionHeader: {
    ...AmplifyTheme.sectionHeader,
    backgroundColor: '#ff6600'
    
  }
};

let params = {
  particles: {
    number: {
      value: 40,
      density: {
        enable: true,
        value_area: 800
      }
    },
    color: {
      value: ["#c311e7", "#b8e986", "#4dc9ff", "#ffd300", "#FF7E79"]
    },
    shape: {
      type: "circle",
      stroke: {
        width: 0,
        color: "#000000"
      },
      polygon: {
        nb_sides: 5
      },
      image: {
        src: "img/github.svg",
        width: 100,
        height: 100
      }
    },
    opacity: {
      value: 0.9,
      random: false,
      anim: {
        enable: false,
        speed: 1,
        opacity_min: 0.5,
        sync: false
      }
    },
    size: {
      value: 8,
      random: true,
      anim: {
        enable: false,
        speed: 30,
        size_min: 0.1,
        sync: false
      }
    },
    line_linked: {
      enable: true,
      distance: 80,
      color: "#ffffff",
      opacity: 0.4,
      width: 1
    },
    move: {
      enable: true,
      speed: 3,
      direction: "none",
      random: false,
      straight: false,
      out_mode: "bounce",
      bounce: false,
      attract: {
        enable: false,
        rotateX: 600,
        rotateY: 1200
      }
    }
  },
  interactivity: {
    detect_on: "canvas",
    events: {
      onhover: {
        enable: true,
        mode: "repulse"
      },
      onclick: {
        enable: true,
        mode: "push"
      },
      resize: true
    },
    modes: {
      grab: {
        distance: 400,
        line_linked: {
          opacity: 1
        }
      },
      bubble: {
        distance: 400,
        size: 40,
        duration: 2,
        opacity: 8,
        speed: 3
      },
      repulse: {
        distance: 150,
        duration: 1
      },
      push: {
        particles_nb: 3
      },
      remove: {
        particles_nb: 2
      }
    }
  },
  retina_detect: true
};


class App extends Component {

  state = {
    imageName: "",
    imageFile: "",
    response: ""
  };

 

  
  handleComplete(err, confirmation) {
    if (err) {
      alert('Bot conversation failed')
      return;
    }

    alert('Success: ' + JSON.stringify(confirmation, null, 2));
    return 'Thank you for using SuppBot! Should you require more assistance, Please contact ACRA!';
  }

  render() {
    return (
  
      <div className="App">
        

        <AmplifySignOut button-text="Sign Out"></AmplifySignOut>
        <header className="App-header">
          <h1 className="App-title">Welcome to SuppBot!</h1>
          <h2>Live Smart Singapore Hackathon(ACRA)</h2>
          <h2>By Team SPx</h2>
        </header>
        <div id="List">
          <h2 className="instructions">Instructions to submit a waiver appeal</h2>
            <ol >
              <li>Ask SuppBot for the link to download the waiver form</li>
              <li>Submit the form with the uploader below</li>
              <li>You will then be notified of the status within minutes</li>
              <li>If you do not receive an email, please double check the email in the form you submitted</li>
              <li>If you still did not receive an email, Please proceed to contact ACRA</li>
              <li>Alternatively, you can choose to schedule an appointment with ACRA by using SuppBot</li>
              <li>Just type "Schedule an appointment" and answer the prompts given by the bot</li>
            </ol>
        </div>
        

      
        <div id="Upload">
        <h2 className= 'UploadHeader'>Upload your completed form here</h2>
        <input
          type="file"
          //accept="image/png, image/jpeg, pdf" This is used to limit to specific file
          style={{ display: "none" }}
          ref={ref => (this.upload = ref)}
          onChange={e =>
            this.setState({
              imageFile: this.upload.files[0],
              imageName: this.upload.files[0].name
            })
          }
        />
        <input value={this.state.imageName} placeholder="Select file" />
        <button
          onClick={e => {
            this.upload.value = null;
            this.upload.click();
          }}
          loading={this.state.uploading}
        >
          Browse
        </button>

        <button onClick={this.uploadImage}> Upload File </button>

        {!!this.state.response && <div>{this.state.response}</div>}
        </div>

     <div id="particles-js" ><Particles style={{position: 'absolute',top: 0,left: 0,right: 0,bottom: 0, zIndex: -1}} params={params} /></div>
     


      </div>
      
    );
  }
}
export default withAuthenticator(App, {includeGreetings:true});