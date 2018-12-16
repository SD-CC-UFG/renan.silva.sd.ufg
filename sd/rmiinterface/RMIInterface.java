package com.sd.rmiinterface;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.ArrayList;

public interface RMIInterface extends Remote {
	public String buscarBroker() throws RemoteException;
	public String inscreverBroker(String ipBroker, String tipo) throws RemoteException;
	public ArrayList<String> listaAdjacencia(String ipBroker, String tipo) throws RemoteException;
}