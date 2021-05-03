import logo from "./logo.svg";
import "./App.css";
import { TextField, Button } from "@contentful/forma-36-react-components";
import "@contentful/forma-36-react-components/dist/styles.css";

function App() {
  return (
    <div className="App">
      <aside className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h4>Hey there, why don't you try logging in?</h4>
      </aside>
      <main>
        <header>
          <p>
            Not a member?
            <a href="https://localhost"> Sign up now</a>
          </p>
        </header>
        <div className="container">
          <form action="">
            <h2 className="title">Sign in here</h2>
            <Button>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                aria-labelledby="fr6gzqks1vhcbf6piwt5uqrcolk3oq6"
                role="img"
                viewBox="0 0 24 24"
                class="icon "
              >
                <title id="fr6gzqks1vhcbf6piwt5uqrcolk3oq6">Google icon</title>
                <path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z"></path>
              </svg>
              Sign in with Google
            </Button>
            <hr className="divider" />
            <div className="input-container">
              <label className="field-label">Username or Email Address</label>
              <TextField />
            </div>
            <div className="input-container">
              <label className="field-label">Password</label>
              <TextField />
            </div>
            <Button>Sign in</Button>
          </form>
        </div>
      </main>
    </div>
  );
}

export default App;
