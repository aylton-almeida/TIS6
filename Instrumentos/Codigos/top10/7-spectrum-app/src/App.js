import logo from './logo.svg';
import './App.css';
import { Provider, defaultTheme, Text, Button, Link, TextField, Flex } from '@adobe/react-spectrum';

const title = {
  fontSize: '24px'
}

function App() {
  return (
    <Provider theme={defaultTheme} colorScheme="light">
      <div className="App">
        <aside className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
                Hey there, why don't you try logging in?
            </aside>
        <main>
          <header>
            <Text>
              Not a member? 
                <Link href="https://react-spectrum.adobe.com/react-spectrum/">Sign up now</Link>
            </Text>
          </header>
          <div className="container">
            <form action="">
              <Flex alignItems="start">
                <Text className="title" UNSAFE_style={title}>
                  Sign in here
                </Text>
              </Flex>
              <Button variant="primary">
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
              <Flex className="input-container">
                <TextField label="Username or Email Address" className="field-label" width="100%"/>
              </Flex>
              <Flex className="input-container" alignItems="start">
                <TextField label="Password" className="field-label" width="100%"/>
              </Flex>
              <Button variant="primary">
                Sign in
              </Button>
            </form>
          </div>
        </main>
      </div>
    </Provider>
  );
}

export default App;
