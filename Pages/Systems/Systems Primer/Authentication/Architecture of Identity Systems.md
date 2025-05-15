Source:
https://www.windley.com/archives/2020/09/the_architecture_of_identity_systems.shtml


_**Introductory note:** I recently read a paper from Sam Smith, [Key Event Receipt Infrastructure](https://arxiv.org/abs/1907.02143), that provided inspiration for a way to think about and classify identity systems. In particular his terminology was helpful to me. This blog post uses terminology and ideas from Sam's paper to classify and analyze three different identity system architectures. I hope it provides a useful model for thinking about identity online._

John Locke was an English philosopher who thought a lot about power: who had it, how it was used, and how it impacted the structure of society. Locke’s theory of mind forms the foundation for our modern ideas about identity and independence. Locke argued that "sovereign and independent" was man’s natural state and that we gave up freedom, our sovereignty, in exchange for something else, protection, sociality, and commerce, among others. This grand bargain forms the basis for any society.

This question of power and authority is vital in identity systems. We can ask "what do we give up and to whom in a given identity system?" More succinctly we ask: _who controls what?_ In [Authentic Digital Relationships](https://www.windley.com/archives/2020/08/authentic_digital_relationships.shtml) I made the argument that self-sovereign identity, supporting heterarchical (peer-to-peer) interaction, enables rich digital relationships that allow people to be digitally embodied so they can act online as autonomous agents. I argued that the architecture of SSI, its structure, made those relationships more authentic.

In this post, I intend to explore the details of that architecture so we can better understand the legitimacy of SSI as an identity system for online interaction. Wikipedia [defines _legitimacy_](https://en.wikipedia.org/wiki/Legitimacy_(political)) as

> the right and acceptance of an authority, usually a governing law or a regime.

While the idea of legitimacy is most often applied to governments, I think we can rightly pose legitimacy questions for technical systems, especially those that function in an authoritative manner and have large impacts on people and society. Without legitimacy, people and organizations using an identity system will be unable to act because anyone they interact with will not see that action as authorized. My thesis is that SSI provides a more legitimate basis for online identity than administrative identity systems of the past.

## Terminology

While we properly talk of identity systems, identity systems do not manage identities, but rather relationships. Identity systems provide the means necessary for _remembering, recognizing, and relying on the other parties to the relationship_. To do so, they use **identifiers**, convenient handles that name the thing being remembered. Identifiers are unique within some **namespace**. The namespace gives context to the identifiers since the same string of characters might be a phone number in one system and a product ID in another.

[![Figure 1: Binding of controller, authentication factors, and identifiers in identity systems.](https://www.windley.com/archives/2020/09/Binding.png "Figure 1: Binding of controller, authentication factors, and identifiers in identity systems.")](https://www.windley.com/archives/2020/09/Binding.png)

Figure 1: Binding of controller, authentication factors, and identifiers in identity systems. (click to enlarge)

Identifiers are issued to or created by a **controller** who by virtue of knowing the **authentication factors** can make authoritative statements about the identifier (e.g. claiming it by logging in). The controller might be a person, organization, or software system. The controller might be the subject that the identifier refers to, but not necessarily. The authentication factors might be a password, key fob, cryptographic keys, or something else. The strength and nature of the **bindings** between the controller, authentication factors, and identifier determine the strength and nature of the relationships built on top of them.

To understand why that's so, we introduce the concept of a **root of trust**1. A root of trust is a foundational component or process in the identity system that is relied on by other components of the system and whose failure would compromise the integrity of the bindings. A root of trust might be primary or secondary depending on whether or not it is replaceable. Primary roots of trust are irreplaceable. Together, the roots of trust form the **trust basis** for the system.

The trust basis enabled by the identity system underlies a particular **trust domain**. The trust domain is the set of digital activities that depend on the binding of the controller to the identifier. For example, binding a customer to an identifier allows Amazon to trust that the actions linked to the identifier are authorized by the controller. Another way to look at this is that the strength of the binding between the identifier and customer (controller) determines the risk that Amazon assumes in honoring those actions.

The strength of the controller-identifier binding depends on the strength of the binding between the controller and the authentication factors and between the authentication factors and the identifier. Attacking either of those bindings reduces the trust we have in the controller-identifier binding and increases the risk that actions taken through a particular identifier are unauthorized.

## Identity Architectures

We can broadly classify identity systems into one of three types based on their architectures and primary root of trust:

- Administrative
- Algorithmic
- Autonomic

Both algorithmic and autonomic are SSI systems. They are distinguished by their trust bases. Some SSI systems use one or the other and some (like Sovrin) are hybrid, employing each for different purposes. We'll discuss the properties of the trust basis for each of these in an effort to understand the comparative legitimacy of SSI solutions to traditional administrative ones.

These architectures differ in who controls what and that is the primary factor in determining the basis for trust in them. We call this **control authority**. The entity with control authority takes action through operations that affect the creation (inception), updating, rotation, revocation, deletion, and delegation of the authentication factors and their relation to the identifier. How these events are ordered and their dependence on previous operations is important. The record of these operations is the **source of truth** for the identity system.

### Administrative Architecture

Identity systems with an administrative architecture rely on an administrator to bind the identifier to the authentication factors. The administrator is the primary root of trust for any domain with an administrative architecture. Almost every identity system in use today has an administrative architecture and their trust basis is founded on the administrator.

[![Figure 2: The trust basis in administrative identity systems.](https://www.windley.com/archives/2020/09/Administrative.png "Figure 2: The trust basis in administrative identity systems.")](https://www.windley.com/archives/2020/09/Administrative.png)

Figure 2: The trust basis in administrative identity systems. (click to enlarge)

Figure 2 shows the interactions between the controller, identifier and authentication factors in an administrative identity system, the role of the administrator, and the impact these have on the strength of the bindings. The controller usually generates the authentication factors by choosing a password, linking a two-factor authentication (2FA) mechanism, or generating keys.

Even though the identifier might be the controller's email address, phone number, public key, or other ID, the administrator "assigns" the identifier to the controller because it is their policy that determines which identifiers are allowed, whether they can be updated, and their legitimacy within the identity system's domain. The administrator "owns" the identifier within the domain. The administrator also asserts the binding between the identifier and the authentication factors. An employee's mistake, a policy change, or a hack could affect the binding between the identifier and authentication factors or the identifier and the controller. Consequently, these bindings are relatively weak. Only the binding between the controller and authentication factors is strong because the controller generates them.

The administrator's primary duty is to authoritatively assert the controller-identifier binding. Authoritative control statements about the identifier are recorded in the administrator's database, the source of truth in the system, subject to change by employees and hackers. The administrator might be an ecommerce site that maintains an identity system as the basis for its customer's account. In this case the binding is private, and its integrity is of interest only to the web site and the customer. Alternatively, the administrator might provide federated login services. In this case the administrator is asserting the controller-identifier binding in a semi-public manner to anyone who relies on the federated login. A certificate authority is an example of an administrator who publicly asserts the controller-identifier binding, signing a certificate to that effect.

Because the administrator is responsible for binding the identifier to both the authentication factors and the controller, the administrator is the primary root of trust and thus the basis for trust in the overall system. Regardless of whether the binding is private, semi-public, or public, the integrity of the binding is entirely dependent on the administrator and the strength of their infrastructure, policies, employees, and continued existence. The failure of any of those can jeopardize the binding, rendering the identity system unusable by those who rely on it.

### Algorithmic Architecture

Identity systems that rely on a ledger have an algorithmic architecture. I'm using "ledger" as a generic term for any algorithmically controlled distributed consensus-based datastore including public blockchains, private blockchains, distributed file systems, and others. Of course, it's not just algorithms. Algorithms are embodied in code, written by people, running on servers. How the code is written, its availability to scrutiny, and the means by which it is executed all impact the trust basis for the system. "Algorithmic" is just shorthand for all of this.

[![Figure 3: The trust basis in algorithmic identity systems.](https://www.windley.com/archives/2020/09/Algorithmic.png "Figure 3: The trust basis in algorithmic identity systems.")](https://www.windley.com/archives/2020/09/Algorithmic.png)

Figure 3: The trust basis in algorithmic identity systems. (click to enlarge)

Figure 3 shows how the controller, authentication factors, identifier, and ledger are bound in an identity system with an algorithmic architecture. As in the administrative identity system, the controller generates the authentication factors, albeit in the form of a public-private key pair. The controller keeps and does not share the private key. The public key, on the other hand, is used to derive an identifier (at least in well-designed SSI systems) and both are registered on the ledger. This registration is the inception of the controller-identifier binding since the controller can use the private key to assert her control over the identifier as registered on the ledger. Anyone with access to the ledger can determine algorithmically that the controller-identifier binding is valid.

The controller makes authoritative control statements about the identifier. The events marking these operations are recorded on the ledger which becomes the source of truth for anyone interested in the binding between the identifier and authentication factors.

In an identity system with an algorithmic trust basis, computer algorithms create a ledger that records the key events. The point of the ledger is that no party has the power to unilaterally decide whether these records are made, modified, or deleted and how they're ordered. Instead, the system relies on code executed in a decentralized manner to make these decisions. The nature of the algorithm, the manner in which the code is written, and the methods and rules for its execution all impact the integrity of the algorithmic identity system and consequently any bindings that it records.

### Autonomic Architecture

Identity systems with an autonomic architecture function similarly to those with an algorithmic architecture. As shown in Figure 4, the controller generates a public-private key pair, derives a globally unique identifier, and shares the identifier and the currently associated public key with anyone.

[![Figure 4: Trust basis in autonomic identity systems.](https://www.windley.com/archives/2020/09/Autonomic.png "Figure 4: Trust basis in autonomic identity systems.")](https://www.windley.com/archives/2020/09/Autonomic.png)

Figure 4: Trust basis in autonomic identity systems. (click to enlarge)

The controller uses her private key to authoritatively and non-repudiably sign statements about the operations on the keys and their binding to the identifier, storing those in an ordered key event log2. One of the important realizations that make autonomic identity systems possible is that the key event log must only be ordered in the context of a single identifier, not globally. So, a ledger is not needed for recording operations on identifiers that are not public. The key event log can be shared with and verified by anyone who cares to see it.

The controller also uses the private key to sign statements that authenticate herself and authorize use of the identifier. A digital signature also provides the means of cryptographically responding to challenges to prove her control of the identifier. These self-authentication and self-authorization capabilities make the identifier self-certifying and self-managing, meaning that there is no external third party, not even a ledger, needed for the controller to manage and use the identifier and prove to others the integrity of the bindings between herself and the identifier. Thus anyone (any entity) can create and establish control over an identifier namespace in a manner that is independent, interoperable, and portable without recourse to any central authority. _Autonomic identity systems rely solely on self-sovereign authority._

Autonomic identifiers have a number of advantages:

- **Self-Certification**—autonomic identifiers are self-certifying so there is no reliance on a third party.
- **Self-Administration**—autonomic identifiers can be independently administered by the controller.
- **Cost**—autonomic identifiers are virtually free to create and manage.
- **Security**—because the keys are decentralized, there is no trove of secrets that can be stolen.
- **Regulatory**—since autonomic identifiers need not be publicly shared or stored in an organization’s database, regulatory concern over personal data can be reduced.
- **Scale**—autonomic identifiers scale with the combined computing capacity of all participants, not some central system.
- **Independent**—autonomic identifiers are not dependent on any specific technology or even being online.

## Algorithmic and Autonomic Identity In Practice

We are all familiar with administrative identity systems. We use them all the time. Less familiar are algorithmic and autonomic identity systems. Their use is emerging under the title of [self-sovereign identity](https://www.windley.com/archives/2020/06/what_is_ssi.shtml).

There are several parallel development efforts supporting algorithmic and autonomic identifiers. The [Decentralized Identifier specification](https://www.w3.org/TR/did-core/) is the primary guide to algorithmic identifiers that live on a ledger. The DID specification provides for many _DID methods_ that allow DIDs to live on a variety of data stores. There's nothing in the DID specification itself that requires that the data store be a blockchain or ledger, but that is the primary use case.

I've [written about the details of decentralized identifiers](https://www.windley.com/archives/2019/02/decentralized_identifiers.shtml) before. DIDs have a number of important properties that make them ideal as algorithmic identifiers. Specifically, they are non-reassignable, resolvable, cryptographically verifiable, and decentralized.

As algorithmic identifiers, DIDs allow the controller to cryptographically make authoritative statements about the identifier and the keys it is bound to. Those statements are recorded on a ledger or blockchain to provide a record of the key events that anyone with access to the ledger can evaluate. The record is usually public since the purpose of putting them on a ledger is to allow parties who don't have an existing relationship to evaluate the identifier and its linkage to the controller and public keys.

There are two related efforts for autonomic identifiers. [Key Event Receipt Infrastructure](https://arxiv.org/abs/1907.02143) is a general-purpose self-certifying system for autonomic identifiers. KERI identifiers are strongly bound at inception to a public-private key pair. All operations on the identifier are recorded in a cryptographic key event log. KERI has strong security and accountability properties. Drummond Reed has made a [proposal that would allow KERI autonomic identifiers to be used with any DID method](https://docs.google.com/presentation/d/1_564J1B3LfBHc_FQnO8jUMiYEx084LVUsHsY1mYPa6U/edit#slide=id.g9398465ffb_33_0).

The second option is [Peer DIDs](https://identity.foundation/peer-did-method-spec/index.html). The vast majority of relationships between people, organizations, and things need not be public and thus have no need for the ability to publicly resolve the DID. Peer DIDs fill this need with the benefits of autonomic identifiers listed above.

Like KERI, Peer DIDs maintain a key event log (called "deltas") that records the relevant operations on the keys in a cryptographic manner. The Peer DID key event log can be shared with other parties in the relationship over [DIDComm](https://identity.foundation/working-groups/did-comm.html), a protocol that allows parties to a relationship to securely and privately share authenticated messages. The [security and authority of a DIDComm channel](https://www.windley.com/archives/2019/06/did_messaging_a_batphone_for_everyone.shtml) are rooted in DIDs and their associated authentication factors. DIDComm can be used over a wide variety of transports.

The vast majority of digital relationships are peer to peer and should use autonomic identifiers. Algorithmic identifiers allow for public discovery of identifier properties when relationships are not peer to peer. In the [Sovrin Network](https://sovrin.org/)3, the ledger records public DIDs for [verifiable credential](https://www.windley.com/archives/2018/12/verifiable_credential_exchange.shtml) issuers. But people, organizations, and things form relationships using peer DIDs without need for the ledger. This hybrid use of both algorithmic and autonomic identity systems was designed so that credential exchange would be practical, secure, and private while reducing the correlation that might occur if individuals used a few DIDs on a ledger.

## Comparing Identity Architectures

Table 1 summarizes the architectural properties of identity systems with administrative, algorithmic, and autonomic bases of trust.

[![Architectural properties of administrative, algorithmic, and autonomic identity systems](https://www.windley.com/archives/2020/09/Architecture%20Comparison.png "Architectural properties of administrative, algorithmic, and autonomic identity systems")](https://www.windley.com/archives/2020/09/Architecture%20Comparison.png)

Table 1: Architectural properties of administrative, algorithmic, and autonomic identity systems (click to enlarge)

The table shows how the locus of control, source of truth, root of trust, and trust basis differ for each of our three architectures. For Administrative systems, the administrator is directly in control of all four of these. In an algorithmic architecture, the controller is the locus of control because the ledger is set up to allow the controller to be in charge of all key operations. Sometimes this is done using special administrative keys instead of the keys associated with the identifier. The organizations or people operating nodes on the ledger [never have access to the keys necessary to unilaterally change the record of operations](https://www.windley.com/archives/2019/07/answering_questions_about_self-sovereign_identity.shtml). No third party is involved in autonomic identity systems.

Table 2 summarizes the trust bases of administrative, algorithmic, and autonomic identity systems4.

[![Comparing the trust bases of administrative, algorithmic, and autonomic identity systems](https://www.windley.com/archives/2020/09/Trust%20Basis%20Comparison.png "Comparing the trust bases of administrative, algorithmic, and autonomic identity systems")](https://www.windley.com/archives/2020/09/Trust%20Basis%20Comparison.png)

Table 2: Summarizing the trust bases of administrative, algorithmic, and autonomic identity systems (click to enlarge)

We can see from the evaluation that algorithmic and autonomic architectures are decentralized while the administrative system has a single point of failure—the third party administrator. As a result administrative systems are less secure since an attack on one party can yield a trove of valuable information. Administrative systems also rely on privacy by policy rather than having privacy preserving features built into the architecture. And, as we've seen, all too often privacy is in direct conflict with the administrator's profit motive leading to weak privacy policies.

## Power and Legitimacy

I started this post by talking about power and legitimacy. From our discussion and the summary tables above, we know that power is held very differently in these three systems. In an administrative system, the administrator holds all the power. I argued in [Authentic Digital Relationships](https://www.windley.com/archives/2020/08/authentic_digital_relationships.shtml) that the architecture of our identity systems directly impacts the quality and utility of the digital relationships they support. Specifically, the power imbalance inherent in administrative identity systems yields anemic relationships. In contrast, the balance of power engendered by SSI systems (both algorithmic and autonomic) yields richer relationships since all parties can contribute to it.

Clearly, administrative identity systems have legitimacy—if they didn't, no one would use or trust them. As new architectures, algorithmic and autonomic systems have yet to prove themselves through usage. But we can evaluate each architecture in terms of the promises it makes and how well it does in the purposes of an identity system: recognizing, remembering, and relying on other parties in the relationship. These are largely a function of the trust basis for the system.

Administrative systems promise an account for taking actions that the administrator allows. They also promise these accounts will be secure and private. But people and organizations are increasingly concerned with privacy and seemingly non-stop security breaches are chipping away at that legitimacy. As noted above, the privacy promise is often quite limited. Since the administrator is the basis for trust, administrative systems allow the administrator to recognize, remember, and rely on the identifier depending on their security. But the account holder does not get any support from the administrative system in recognizing, remembering, or relying on the administrator. The [relationship is strictly one-way and anemic](https://www.windley.com/archives/2020/08/authentic_digital_relationships.shtml).

SSI systems promise to give anyone the means to securely and privately create online relationships and trustworthily share self-asserted and third-party-attested attributes with whoever they chose. These promises are embodied in the [property I call fidelity](https://www.windley.com/archives/2019/10/fidelity_provenance_and_trust.shtml). To the extent that algorithmic and autonomic identity systems deliver on these promises, they will be seen as legitimate.

Both algorithmic and autonomic identity systems provide strong means for recognizing, remembering, and relying on the identifiers in the relationship. For an algorithmic system, we must trust the ledger as the primary root of trust and the trust basis. Clearly our trust in the ledger will depend on many factors, including the code and the [governance that controls its operation](https://www.windley.com/archives/2018/02/decentralized_governance_in_sovrin.shtml).

The trust basis for an autonomic identity system is cryptography. This implies that digital key management will become an important factor in its legitimacy. If people and organizations cannot easily manage the keys in such a system, then it will not be trusted. There is hope that key management can be solved since the primary artifacts that people using an SSI system manipulate are relationships and credentials, not keys and secrets. By supporting a consistent user experience rooted in familiar artifacts from the physical world, SSI promises to make cryptography a usable technology by the majority of people on the Internet.

## Conclusion

In this article, we've explored the high-level architectures for the identity systems in use today as well as new designs that promise richer, more authentic online relationships, better security, and more privacy. By exploring the trust bases that arise from these architectures we've been able to explore the legitimacy of these architectures as a basis for online identity. My belief is that a hybrid system that combines algorithmic public identifiers with autonomic private identifiers can provide a universal identity layer for the Internet, increasing security and privacy, [reducing friction](https://www.windley.com/archives/2019/08/life-like_identity_why_the_internet_needs_an_identity_metasystem.shtml), and providing [new](https://www.windley.com/archives/2018/08/youve_had_an_automobile_accident_multi-source_identity_to_the_rescue.shtml) and [better](https://www.windley.com/archives/2020/06/held_hostage.shtml) online experiences.

---

### Notes

1. Often the term _root of trust_ is used to a hardware device or some trusted hardware component in the computer. The usage here is broader and refers to anything that is relied on for trust in the identity system. _Trust anchor_ is a term that has sometimes been used in the cryptography community to refer to this same concept.
2. A number of cryptographic systems are trivially self-certifying (e.g. PGP, Ethereum, Bitcoin, etc.). What sets the autonomic identity systems described here apart is the key event log. Sam Smith calls these identifiers “autonomic identifiers” to set them apart from their less capable counterparts and emphasize their ability to self-manage keys without recourse to a third party system.
3. The Sovrin Network is an operational instance of the code found in the Hyperledger [Indy](https://www.hyperledger.org/use/hyperledger-indy) and [Aries](https://www.hyperledger.org/use/aries) projects.
4. This table is borrowed, with permission, from Chapter 10 of the upcoming Manning publication [Self-Sovereign Identity](https://www.manning.com/books/self-sovereign-identity) by Drummond Reed and Alex Preukschat.



