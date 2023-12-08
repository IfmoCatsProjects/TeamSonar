interface UserData {
	id: number;
    username: string;
    common_games: { name: string }[];
    description: string;
	avatar_url: string;
}

const acc : HTMLElement | null= document.getElementById('accept');
const dec : HTMLElement | null= document.getElementById('decline');

let globalData: UserData[] = [];

async function localFetch () {
	const data = await fetchData();
	console.log(data);
	globalData = data;
	updateList(globalData);
	return data;
}

function createElementFromString(htmlString: string): HTMLElement {
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmlString, 'text/html');
    return doc.body.firstChild as HTMLElement;
}

let i: number = 0;

function cardData(user: UserData): HTMLDivElement {
    const ret: HTMLDivElement = document.createElement('div');
    ret.className = 'card';

    const cardLeft: HTMLDivElement = document.createElement('div');
    const cardRight: HTMLDivElement = document.createElement('div');

    cardLeft.innerHTML = `<h1>${user.username}</h1><p>${user.description}</p>`;
	cardLeft.className = 'card_description';
	console.log(`${user.common_games[0]}`);
    cardRight.innerHTML = `<h1>ИГРЫ</h1><p>${user.common_games[0]}</p>`;
	//for (let i: number = 0; i < user.common_games.length; i++) {
	//	cardRight.innerHTML += `<p>${user.common_games[i].name}</p>`;
	//}

    
    ret.style.backgroundImage = `url(${user.avatar_url})`;
	ret.style.backgroundSize = 'cover';
    ret.appendChild(cardLeft);
    ret.appendChild(cardRight);

    return ret;
}

function updateList(data: UserData[]): void {
    const suggestions = document.getElementById('card-holder');
    if (!suggestions) {
        console.error('Element with id "suggestions" not found.');
        return;
    }
    suggestions.innerHTML = '';
    const divItem = cardData(data[i]);
    suggestions.innerHTML = '';
    suggestions.appendChild(divItem);
    i++;
}

async function fetchData() {
    try {
        const response = await fetch('suggestions');

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const contentType = response.headers.get('content-type');

        if (!contentType || !(contentType.trim() === 'application/json')) {
            throw new Error('Invalid content type. Expected JSON.');
        }

        const data: UserData[] = await response.json();
        return data;
    } catch (error) {
        console.error('ERROR: ', error);
        throw error;
    }
}

function decceptGet(acc: boolean) {
  const params = new URLSearchParams({
    'accept': acc.toString(),
    'viewed_id': globalData[i].id.toString()
  });

  fetch(`collide?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      return response.text();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.error('ERROR:', err.message);
    });
}


if (acc) acc.onclick = () => {
	decceptGet (true);
	updateList(globalData);
}

if (dec) dec.onclick = () => {
	decceptGet (false);
	updateList(globalData); 
}

localFetch();
