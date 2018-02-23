from flask import render_template, abort
from flask_login import login_required
from app import app, db
from app.models import Onions, Links


@app.route("/", methods=["GET"])
# @login_required
def index():
    # Retrieve link information, then build visual representation.
    # Get the list of domains.
    output = ''
    domain_list = db.session.query(Onions.id, Onions.domain).filter(Onions.online == True,
                                                                    Onions.scan_date != '1900-01-01').all()

    # Get the list of links.
    link_list = db.session.query(Links.domain_from, Links.domain_to).filter(
        Links.domain_from.in_(
            db.session.query(Onions.domain).filter(Onions.online == True, Onions.scan_date != '1900-01-01')),
        Links.domain_to.in_(
            db.session.query(Onions.domain).filter(Onions.online == True, Onions.scan_date != '1900-01-01'))).all()

    if not domain_list or not link_list:
        return render_template("base.html", new_body=output)

    # Compile the domain dictionary.
    domains = {}
    for result in domain_list:
        (domain_id, domain_name) = result
        domains[domain_id] = domain_name

    # Compile the link list.
    links = []
    linked_domains = []
    for link in link_list:
        (link_from, link_to) = link
        if link_from != link_to:
            # We only want links that don't refer to themselves.
            linked_domains.append(link_from)
            linked_domains.append(link_to)
            links.append([link_from, link_to])
    linked_domains = list(set(linked_domains))

    # Design output
    output_list = []
    output_list.append('<script language="javascript">')
    for domain in domains.keys():
        if domain in linked_domains:
            output_list.append("graph.addNode({}, '{}');".format(
                domain, domains[domain]))
    for link in links:
        [link_from, link_to] = link
        output_list.append("graph.addLink({}, {});".format(
            link_from, link_to))
    output_list.append('var renderer = Viva.Graph.View.renderer(graph);')
    output_list.append('</script>')
    # TODO: Instead of generating HTML simply generate the list of items and pass it to jinja to automatically create the HTML
    # Create HTML

    for item in output_list:
        output += ' '.join(item.split())

    return render_template("base.html", new_body=output)
