import logo from './logo.svg';
import './App.css';
import { Client as Styletron } from 'styletron-engine-atomic';
import { Provider as StyletronProvider } from 'styletron-react';
import { LightTheme, BaseProvider } from 'baseui';
import { Button } from "baseui/button";
import { Input } from "baseui/input";
import { DisplayMedium, LabelMedium } from 'baseui/typography';
import { StyledLink } from "baseui/link";

const engine = new Styletron();

function App() {
  return (
    <StyletronProvider value={engine}>
      <BaseProvider theme={LightTheme}>
        <div className="App">
          <aside className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
              Hey there, why don't you try logging in?
          </aside>
          <main>
            <header>
              <LabelMedium>
                Not a member?
                <StyledLink href="https://baseweb.design/getting-started/setup/"> Sign up now</StyledLink>
              </LabelMedium>
            </header>
            <div className="container">
              <form action="">
                <DisplayMedium className="title">
                  Sign in here
                </DisplayMedium>
                <Button>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    aria-labelledby="fr6gzqks1vhcbf6piwt5uqrcolk3oq6"
                    role="img"
                    viewBox="0 0 24 24"
                  >
                    <title id="fr6gzqks1vhcbf6piwt5uqrcolk3oq6">Google icon</title>
                    <path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z"></path>
                  </svg>
                  Sign in with Google
                </Button>
                <hr className="divider" />
                <div className="input-container">
                  <LabelMedium className="field-label">
                    Username or Email Address
                  </LabelMedium> 
                  <Input/>
                </div>
                <div className="input-container">
                  <LabelMedium className="field-label">
                    Password
                  </LabelMedium>
                  <Input/>
                </div>
                <Button>
                  Sign in
                </Button>
              </form>
            </div>
          </main>
        </div>
      </BaseProvider>
    </StyletronProvider>
  );
}

export default App;
