import * as React from 'react';
import {Mutation} from 'react-apollo';
import gql from 'graphql-tag';
import {IUserLogin, IUser} from '../../types/user';

const MUTATION = gql`
  mutation login($username: String!, $password: String!) {
    getToken(username: $username, password: $password) {
      token
      user {
        id
        username
        email
        account
      }
    }
  }
`;

interface IData {
  getToken: {
    token: string;
    user: IUser;
  };
}

interface IVariables extends IUserLogin {}

const Login = () => {
  const [fields, setField] = React.useState({
    username: '',
    password: ''
  });

  const handleInput = (e: React.FormEvent<HTMLInputElement>) => {
    const {name, value} = e.currentTarget;
    setField({...fields, [name]: value});
  };

  return (
    <div>
      <Mutation<IData, IVariables>
        mutation={MUTATION}
        variables={{...fields}}
        update={(cache, {data}) => {
          localStorage.setItem('token', data ? data.getToken.token : '');
          cache.writeData({data: {currentUser: data && data.getToken.user}});
        }}
      >
        {(login, {loading, error, data}) => {
          const handleSubmit = (e: React.SyntheticEvent) => {
            e.preventDefault();
            login({variables: {...fields}});
          };

          return (
            <div>
              <h1>Login Here</h1>
              <form onSubmit={handleSubmit}>
                <div>
                  <input
                    type="text"
                    value={fields.username}
                    name="username"
                    onChange={handleInput}
                    placeholder="Enter username"
                  />
                </div>
                <div>
                  <input
                    type="text"
                    value={fields.password}
                    name="password"
                    onChange={handleInput}
                    placeholder="Enter password"
                  />
                </div>
                <button type="submit">Submit</button>
              </form>
              {loading && <div>Loading...</div>}
              {data && data.getToken && <div>{JSON.stringify(data.getToken)}</div>}
              {error && <div>Something is wrong</div>}
            </div>
          );
        }}
      </Mutation>
    </div>
  );
};

export default Login;
