# Generate Private Key, Public Key and Bitcoin Address

## How to run

1. Clone this repository: `git clone https://github.com/namcoi99/blockchain-course-032021.git`.

2. Change to JavaScript directory: `cd JavaScript`.

3. Install the dependencies: `yarn install` or `npm install`.

4. Run the app: `npm start`.

5. Go to: `http://localhost:4000`

6. Insert this query to automatically generate Private Key, Public Key and Bitcoin Address:
```
{
  getNewKeyPairs {
    address
    publicKey
    privateKey
  }
}
```

7. Have Fun!
