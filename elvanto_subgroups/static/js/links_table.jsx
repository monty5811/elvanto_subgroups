var SubGroup = React.createClass({
  render: function () {
    return (<p>{this.props.subgroup}</p>)
  }
});
var NiceTime = React.createClass({
  render: function () {
    let nicetime = moment(this.props.datetimestr).fromNow();
    return (<div>{nicetime}</div>) 
  }
});
var LinkRow = React.createClass({
  render: function () {
    var subgroupNodes =  this.props.link.sub_groups.map(function (sub_group, index) {
      return (
          <SubGroup subgroup={sub_group} key={index}/>
          )
    });
    return (
        <tr>
        <td><a href={this.props.link.url}>{this.props.link.name}</a></td>
        <td>{subgroupNodes}</td>
        <td><NiceTime datetimestr={this.props.link.last_sync}/></td>
        <td><a href={this.props.link.delete_url} className="btn btn-danger btn-xs">Remove</a></td>
        </tr>
        )
  }
});

var LinksTable = React.createClass({
    loadResponsesFromServer: function () {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function (data) {
                this.setState({data: data});
            }.bind(this),
            error: function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    getInitialState: function () {
        return {data: []};
    },
    componentDidMount: function () {
        this.loadResponsesFromServer();
        setInterval(this.loadResponsesFromServer, this.props.pollInterval);
    },
    render: function () {
        var linkNodes = this.state.data.map(function (link, index) {
                return (
                    <LinkRow link={link} key={index}/>
                    )
        });
        return (
            <table className="table table-condensed table-striped">
            <thead>
            <tr>
            <th>Group</th>
            <th>Subgroups</th>
            <th>Synced</th>
            <th></th>
            </tr>
            </thead>
            <tbody>
            {linkNodes}
            </tbody>
            </table>
        );
    }
});
