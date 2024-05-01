export async function updateUserHandle(handle) {

    if (!isLoggedIn()){
  
      // redirect to login screen
  
      return;
  
    }
  
    let token = localStorage.getItem(jwtKey);
  
    let decodedToken = decodeJWT(token);
  
    const hoursDelta = 24;
  
    if (decodedToken.exp < (Date.now() + hoursDelta*60*60) / 1000){
  
      refreshToken();
  
    }
  
    return await fetch(`${domain}/v1/users/handle`, {
  
      method: 'PUT',
  
      mode: 'cors',
  
      headers: {
  
        'Content-Type': 'application/json',
  
        'Authorization': `Bearer ${token}`
  
      },
  
      body: JSON.stringify({
  
        handle
  
      })
  
    });
  
  }
  
  
  
  export async function updateUserInterests(interestUUIDs) {
  
    if (!isLoggedIn()){
  
      // redirect to login screen
  
      return;
  
    }
  
    let token = localStorage.getItem(jwtKey);
  
    let decodedToken = decodeJWT(token);
  
    const hoursDelta = 24;
  
    if (decodedToken.exp < (Date.now() + hoursDelta*60*60) / 1000){
  
      refreshToken();
  
    }
  
    return await fetch(`${domain}/v1/users/interests`, {
  
      method: 'PUT',
  
      mode: 'cors',
  
      headers: {
  
        'Content-Type': 'application/json',
  
        'Authorization': `Bearer ${token}`
  
      },
  
      body: JSON.stringify({
  
        interestUUIDs
  
      })
  
    });
  
  }
  