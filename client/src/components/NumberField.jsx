import './NumberField.css'

function NumberField({field, ...props}) {
    return (
        <div className="number-field">
            <div className="number-field__title">
                {field.name}
            </div>
            <input type="number" value={field.value} onChange={e => props.onChange(field, e.target.value)} />
        </div>
    )
}

export default NumberField