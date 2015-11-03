"use strict";

var SubGroup = React.createClass({
    displayName: "SubGroup",

    render: function render() {
        return React.createElement(
            "p",
            null,
            this.props.subgroup
        );
    }
});
var NiceTime = React.createClass({
    displayName: "NiceTime",

    render: function render() {
        var nicetime = moment(this.props.datetimestr).fromNow();
        return React.createElement(
            "div",
            null,
            nicetime
        );
    }
});
var LinkRow = React.createClass({
    displayName: "LinkRow",

    render: function render() {
        var subgroupNodes = this.props.link.sub_groups.map(function (sub_group, index) {
            return React.createElement(SubGroup, { subgroup: sub_group, key: index });
        });
        return React.createElement(
            "tr",
            null,
            React.createElement(
                "td",
                null,
                React.createElement(
                    "a",
                    { href: this.props.link.url },
                    this.props.link.name
                )
            ),
            React.createElement(
                "td",
                null,
                subgroupNodes
            ),
            React.createElement(
                "td",
                null,
                React.createElement(NiceTime, { datetimestr: this.props.link.last_sync })
            ),
            React.createElement(
                "td",
                null,
                React.createElement(
                    "a",
                    { href: this.props.link.delete_url, className: "btn btn-danger btn-xs" },
                    "Remove"
                )
            )
        );
    }
});

var LinksTable = React.createClass({
    displayName: "LinksTable",

    loadResponsesFromServer: function loadResponsesFromServer() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: (function (data) {
                this.setState({ data: data });
            }).bind(this),
            error: (function (xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }).bind(this)
        });
    },
    getInitialState: function getInitialState() {
        return { data: [] };
    },
    componentDidMount: function componentDidMount() {
        this.loadResponsesFromServer();
        setInterval(this.loadResponsesFromServer, this.props.pollInterval);
    },
    render: function render() {
        var linkNodes = this.state.data.map(function (link, index) {
            return React.createElement(LinkRow, { link: link, key: index });
        });
        return React.createElement(
            "table",
            { className: "table table-condensed table-striped" },
            React.createElement(
                "thead",
                null,
                React.createElement(
                    "tr",
                    null,
                    React.createElement(
                        "th",
                        null,
                        "Group"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Subgroups"
                    ),
                    React.createElement(
                        "th",
                        null,
                        "Synced"
                    ),
                    React.createElement("th", null)
                )
            ),
            React.createElement(
                "tbody",
                null,
                linkNodes
            )
        );
    }
});