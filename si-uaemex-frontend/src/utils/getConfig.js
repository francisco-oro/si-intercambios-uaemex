
const getConfig = () => ({

    headers: {
        'Authorization': `Bearer ${localStorage.getItem("token")}`
    },
})
console.log(getConfig())

export default getConfig;


export const Connection = 'http://localhost:8001/api/v1/'