import React,{Component} from 'react'
import { TokenAnnotator } from 'react-text-annotate'

// const TEXT = `109277792 109277792 RWH 3477400 810976 7792902 01/30/2004 12:00:00 AM ED Discharge Summary Unsigned DIS ~~~ Report Status ~~~ Unsigned ED DISCHARGE NOTIFICATION / SUMMARY SHUFFSKOCKOTESKI, DRU ~~~ MRN ~~~ 3477400 ~~~ Age ~~~ 51y ~~~ REGISTRATION DATE ~~~ 01/30/2004 01:59 AM ~~~ Provider ~~~ KOMAND SILBEDOUETTLAND PRELIMINARY REPORT ~~~ PCP notified by MD ~~~ No - Other explanation ~~~ Benefits Assigned ~~~ N ~~~ Discharge Date / Time ~~~ 01/30/2004 08:28 ~~~ Discharge Status ~~~ Discharged ~~~ Condition on Discharge ~~~ Stable ~~~ Patient States Complaint ~~~ AGGRAVATED / NEEDS APS EVAL ~~~ Diagnosis ~~~ Impulsivity ~~~ 1` +
//     '109277792 109277792 RWH 3477400 810976 7792902 01/30/2004 12:00:00 AM ED Discharge Summary Unsigned DIS ~~~ Report Status ~~~ Unsigned ED DISCHARGE NOTIFICATION / SUMMARY SHUFFSKOCKOTESKI, DRU ~~~ MRN ~~~ 3477400 ~~~ Age ~~~ 51y ~~~ REGISTRATION DATE ~~~ 01/30/2004 01:59 AM ~~~ Provider ~~~ KOMAND SILBEDOUETTLAND PRELIMINARY REPORT ~~~ PCP notified by MD ~~~ No - Other explanation ~~~ Benefits Assigned ~~~ N ~~~ Discharge Date / Time ~~~ 01/30/2004 08:28 ~~~ Discharge Status ~~~ Discharged ~~~ Condition on Discharge ~~~ Stable ~~~ Patient States Complaint ~~~ AGGRAVATED / NEEDS APS EVAL ~~~ Diagnosis ~~~ Impulsivity ~~~ 1'
// const IMAGE_URL = "https://groundtruthnw.s3.amazonaws.com/raw-abstracts-jpgs/1801_00146.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20190225T225559Z&X-Amz-SignedHeaders=host&X-Amz-Expires=3599&X-Amz-Credential=AKIAISPQWY2DKP2O45RQ%2F20190225%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b5ea9b21298e9780b56f48342a55e88c53e8a5ac44cbcf91e8abeff030b7c8d4"
// const METADATA = "{\n" +
//     "      \"payor_id\": \"Aetna\",\n" +
//     "      \"claim_id\": \"133232\"\n" +
//     "    }";


const TEXT = document.querySelector('#document-text').innerText;
const IMAGE_URL = document.querySelector('#encodedImage').innerText;
const METADATA = document.querySelector('#metadata').innerText;


const TAG_COLORS = {
  ABSTRACT: '#84d2ff',
  TOPIC: '#00ffa2',
}


const Card = ({children}) => (
  <div
    style={{
      boxShadow: '0 2px 4px rgba(0,0,0,.1)',
      margin: 6,
      maxWidth: 600,
      padding: 16,
    }}
  >
    {children}
  </div>
)

class App extends Component{

    constructor(props) {
        super(props);

        this.state = {
            value: [],
            tag: "ABSTRACT",
            support_claim: "",
            notes: "",
            metadata: METADATA,
            numPages: 1,
            pageNumber: 1,
        }
    }

  handleChange = value => {
    this.setState({value});
  }


  handleTagChange = e => {
    this.setState({tag: e.target.value})
  }

  handleYesBtn = e => {
    this.setState({support_claim: "YES"})
  }

  handleNoBtn = e => {
    this.setState({support_claim: "NO"})
  }

  handleNotes = e => {
    this.setState( {notes: e.target.value})
  }

  render() {
    return (

      <div style={{padding: 12, fontFamily: 'sans-serif'}}>

        <div className="row" style={{fontFamily: 'sans-serif'}}>
            <div class="col" style={{maxWidth:"1000px"}}>
              <h3 style={{}}>Instructions</h3>
              <p> The task can be completed with blank, or saved and returned to when time is available to make more
                  progress.
                  If there is evidence in the record to support or deny an audit, <b>highlight</b> it with with the
                  cursor and select <b>Yes</b> or <b>No</b>.
                  Add any notes you have for each task in the <b>Notes</b> free text area.</p>
            </div>
            <div></div>
        </div>
        <div class="row" style={{display: 'flex', marginBottom: 6}}>


          <Card>
              <div class="img_contain">
                <img id="claims_image" name="claims_image" class="page" src={IMAGE_URL} alt="alt"/>
              </div>
          </Card>

          <Card>
            <div class="col-sm-5" style={{paddingLeft:"0px"}}>
                <select class="form-control" onChange={this.handleTagChange} value={this.state.tag}>
                    <option name="ABSTRACT" value="ABSTRACT">ABSTRACT</option>
                    <option name="TOPIC" value="TOPIC">TOPIC</option>
                </select>
            </div>
            <div class="border border-success bg-light">
                 <TokenAnnotator
              style={{
                fontFamily: 'sans-serif',
                maxWidth: 600,
                lineHeight: 1.5,
              }}
              tokens={TEXT.split(' ')}
              value={this.state.value}
              onChange={this.handleChange}
              getSpan={span => ({
                ...span,
                tag: this.state.tag,
                color: TAG_COLORS[this.state.tag],
              })}
              renderMark={props => (
                <mark
                  key={props.key}
                  onClick={() => props.onClick({start: props.start, end: props.end})}
                  color={TAG_COLORS[this.state.tag]}
                >
                  {props.content} [{props.tag}]
                </mark>
              )}
            />
              </div>
            <div class="form-row">
                <div class="col-md-8">
                <h5 class="font-weight-bold">Notes:</h5>
                <textarea className="form-control" rows="5" onChange={this.handleNotes} value={this.state.notes}
                          name="notes" rows="10" cols="80%"> </textarea>
                </div>
                <div class="col">
                    <br></br>
                <h5 class="font-weight-bold">Is this a good Abstract?</h5>
                <div className="col-md-8">
                      <button type="button" onClick={this.handleYesBtn}  className="btn btn-md btn-success btn-block" style={{fontSize:"30px"}} name="y_0">Yes</button>
                </div>
                <br></br>
                <div className="col-md-8">
                      <button type="button" onClick={this.handleNoBtn}  className="btn btn-md btn-danger btn-block" style={{fontSize:"30px"}} name="n_0">No</button>
                </div>
                </div>
            </div>
          </Card>
        </div>
          <pre hidden={true}>{JSON.stringify(this.state, null, 2)}</pre>
          {/*<Card>*/}
          {/*<h4>Current Value</h4>*/}
          {/*<pre hidden={false}>{JSON.stringify(this.state, null, 2)}</pre>*/}
        {/*</Card>*/}
      </div>
    )
  }
}

export default App
