import { Object, Property } from "fabric-contract-api";

@Object()
export class Asset {
    @Property()
    public docType?: string;

    @Property()
    public ID: string;

    @Property()
    public PatientID: string;

    @Property()
    public DoctorID: string;

    @Property()
    public Diagnosis: string;

    @Property()
    public TestsRequested: Array<string>;

    @Property()
    public Perscriptions: Array<string>;

}