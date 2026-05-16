function SignalBadge({signal,confidence}){
    if(!signal){
        return <div className="signal badge signal-badge--empty">No Signal Yet</div>
    }
    const config={
        BUY:{ label:"BUY",className:"signal-badge--buy",icon:"🟢"},
        SELL:{label:"SELL",className:"signal-badge--sell",icon:"🔴"},
        HOLD:{label:"HOLD",className:"signal-badge--hold",icon:"🟡"}
    }

    const {label,className,icon}=config[signal] ?? config.HOLD
    const confidencePct=((confidence??0)*100).toFixed(1)

    return(
        <div className={`signal-badge ${className}`}>
            <span className="signal-badge__icon">{icon} </span>
            <span className="signal-badge__label">{label} </span>
            <span className="signal-badge__confidence">
                {confidencePct}% Confidence
            </span>
        </div>
    )
}

export default SignalBadge