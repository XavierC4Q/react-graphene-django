export interface IUser {
  id: number;
  username: string;
  email: string;
  account: string;
  latitude: number;
  longitude: number;
  search_distance: number;
  __typeName?: string;
}

export interface IUserLogin {
  username: string;
  password: string;
}
