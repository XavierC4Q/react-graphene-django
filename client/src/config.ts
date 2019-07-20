import * as dotenv from 'dotenv';
dotenv.config();

export default {
  GQL_HTTP: process.env.GRAPHQL_HTTP_ENDPOINT
};
