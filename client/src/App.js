import { useEffect, useState } from 'react'
import './App.css'
import BooleanField from './components/BooleanField'
import axios from 'axios'

function App() {

    const [age, setAge] = useState(0)
    const [gender, setGender] = useState(0)
    const [fields, setFields] = useState([])
    const [searchQuery, setSearchQuery] = useState('')
    const [resultQuery, setResultQuery] = useState([])
    const [sortedFields, setSortedFields] = useState([])
    const [result, setResult] = useState('Нет диагноза')
    const [resultIACP, setResultIACP] = useState('')

    useEffect(() => {
        axios.get('/parameters')
            .then(response => {
                setFields(response.data.result)
            })
            .catch(error => {
                console.log(error)
            })
    }, [])

    useEffect(() => {
        const result = fields.map(field => {
            if (field.value) return 1
            return 0
        })
        setResultQuery([gender, age, ...result])
    }, [gender, age,fields])

    useEffect(() => {
        const sorted = fields.filter(field => {
            return field.name.toLowerCase().includes(searchQuery.toLowerCase())
        })
        setSortedFields(sorted)
    }, [fields, searchQuery])

    function checkField(field) {
        const index = fields.indexOf(field)
        fields[index].value = !fields[index].value
        setFields([...fields])

        axios.post('/predict', {
            query: resultQuery
        })
            .then(response => {
                setResult(response.data.result)
            })
            .catch(error => {
                console.log(error)
            })
    }

    function predictIACP() {
        setResultIACP('...')
        axios.post('/iacp/predict', {
            query: resultQuery
        })
            .then(response => {
                setResultIACP(response.data.result.comment)
            })
            .catch(error => {
                console.log(error)
                setResultIACP('')
            })
    }

    function setFieldValue(field, value) {
        const index = fields.indexOf(field)
        value = Number(value)
        if (value > 100) value = 100
        else if (value < 0) value = 0
        fields[index].value = value
        setFields([...fields])
    }

    function clamp(num, min, max) {
        return Math.min(Math.max(num, min), max)
    }

    function setAgeValue(age) {
        setAge(clamp(age, 0, 200))
    }

    return (
        <div className="wrapper">
            <div className="search-panel">
                <input
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                    placeholder="Поиск"
                    className="search-field"
                    type="text"
                />
            </div>
            <div className="common-fields">
                <div className="number-field">
                    <div className="number-field__title">
                        Возраст
                    </div>
                    <input
                        value={age}
                        onChange={e => setAgeValue(e.target.value)}
                        type="number" />
                </div>
                <div className="toggle-field">
                    <div
                        onClick={() => setGender(0)}
                        className={'toggle-field__option ' + (gender === 0 ? 'active' : '')}>
                        Женщина
                    </div>
                    <div
                        onClick={() => setGender(1)}
                        className={'toggle-field__option ' + (gender === 1 ? 'active' : '')}>
                        Мужчина
                    </div>
                </div>
            </div>
            <form className="form">
                {sortedFields.map((field, index) => {
                    return <BooleanField
                        key={index}
                        field={field}
                        onClick={checkField}
                    />
                }
                )
                }
            </form>
            <p className="hint">{resultQuery}</p>
            <p className="hint">{result}</p>
            <div className="iacp-panel">
                <div className="iacp-solver">
                    <button onClick={predictIACP}>IACPaaS</button>
                    <div className="iacp-solver__result">
                        <p>{resultIACP}</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
